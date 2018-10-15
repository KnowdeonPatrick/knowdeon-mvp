from django.shortcuts import render
from student_dashboard.models import Course, Module, SubmitedCourse, Chapter, Section, Item
from django.contrib.auth.decorators import login_required
from knowdeon.forms import SignUpForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.phone_number = form.cleaned_data.get('phone_number')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.email, password=raw_password)
            login(request, user)

            # by default submit course "DESIGN THINKING"  USE ONLY FOR VERSION 1.0

            submited_course = SubmitedCourse.objects.create(user=request.user, course=Course.objects.get(id=4), current_module=1, current_chapter=1, current_section=1, completed=False)

            return redirect('/student_dashboard/index/')
    else:
        form = SignUpForm()
    return render(request, 'student_dashboard/signup.html', {'form': form})

@login_required
def index(request):
    
    user = request.user
    submited_courses = SubmitedCourse.objects.select_related('course').filter(user__id=user.id, is_active=True, course__is_active=True)

    recomended_courses = Course.objects.exclude(submitedcourse__user_id=user.id).filter(is_active=True)
    return render(request, 'student_dashboard/index.html', {'submited_courses': submited_courses, 'recomended_courses' : recomended_courses})

def course_view(request, *args, **kwargs):
    submited_course = SubmitedCourse.objects.select_related('course').get(id=kwargs['pk'])
    modules = Module.objects.filter(course_id=submited_course.course.id).order_by('position')
    chapters = Chapter.objects.select_related('module').filter(module__course_id=submited_course.course.id).order_by('module__position', 'position')
    return render(request, 'student_dashboard/course.html', {'submited_course' : submited_course, 'modules' : modules, 'chapters' : chapters})

def chapter_view(request, *args, **kwargs):
    submited_course = SubmitedCourse.objects.select_related('course').get(id=kwargs['submited_course'])
    chapter = Chapter.objects.select_related('module').get(id=kwargs['chapter_id'])
    sections = Section.objects.select_related('chapter').filter(chapter_id=chapter.id)
    context = {'submited_course' : submited_course, 'chapter': chapter}
    if chapter.module.position == submited_course.current_module  and chapter.position == submited_course.current_chapter:
        # this chapter is not completed yet
        sections = sections.filter(position__lte=submited_course.current_section)
        context['chapter_review'] = False
    else:
        # this chapter was already viewed before
        context['chapter_review'] = True
        next_chapters = Chapter.objects.filter(module__id=chapter.module.id, position=chapter.position + 1).order_by('position')
        if next_chapters:
            context['next_chapter'] = next_chapters[0]
        else:
            context['more_modules'] = Module.objects.filter(id=chapter.module.id + 1).order_by('position')
    context['sections'] = sections
    context['items'] = Item.objects.select_related('section').filter(section__chapter__id=kwargs['chapter_id']) #filter.(section__chapter__module__course_id=submited_course.course.id) 

    return render(request, 'student_dashboard/chapter.html', context)

def next_section(request):
    submited_course_id = request.POST.get('submited_course')

    submited_course = SubmitedCourse.objects.get(id=submited_course_id)
    # if current section < max section.position in the chapter
    more_sections = Section.objects.filter(
        chapter__module__course__submitedcourse__id=submited_course.id,
        chapter__module__position=submited_course.current_module,
        chapter__position=submited_course.current_chapter,
        position__gt=submited_course.current_section,)
    if more_sections:
        next_section = more_sections.get(position=submited_course.current_section + 1)
        submited_course.current_section += 1
        submited_course.save()
        items = Item.objects.filter(section__id=next_section.id)

        return render(request, 'student_dashboard/_section.html', {'submited_course' : submited_course ,'items' : items, 'next_section' : next_section })

    else:
        more_chapters = Chapter.objects.filter(
            module__course__submitedcourse__id=submited_course.id,
            module__position=submited_course.current_module,
            position__gt=submited_course.current_chapter,)
        if more_chapters:
            next_chapter = more_chapters.get(position=submited_course.current_chapter + 1)
            # move to next chapter
            submited_course.current_chapter += 1
            #next chapter, first section
            submited_course.current_section = 1
            submited_course.save()

            return render(request, 'student_dashboard/_next_chapter_button.html', {'submited_course' : submited_course,'next_chapter' : next_chapter})
        
        else:
            more_modules = Module.objects.filter(
                course__submitedcourse__id=submited_course.id,
                position__gt=submited_course.current_module,
            )
            if more_modules:
                next_module = more_modules.get(position=submited_course.current_module + 1)
                # move to next module
                submited_course.current_module += 1
                # next module, first chapter, first section
                submited_course.current_chapter = 1
                submited_course.current_section = 1
                submited_course.save()

                return render(request, 'student_dashboard/_next_module_button.html', {'submited_course' : submited_course})

            else:
                submited_course.completed = True
                submited_course.save()
                # render the Congaratulations page
                return render(request, 'student_dashboard/_completed_course.html', {'submited_course' : submited_course})

def reset_progress(request, *args, **kwargs):
    submited_course = SubmitedCourse.objects.get(id=kwargs['submited_course'])
    submited_course.current_module = 1
    submited_course.current_chapter = 1
    submited_course.current_section = 1
    submited_course.completed = False
    submited_course.save()

    return redirect('/student_dashboard/course/' + str(submited_course.id) + '/')