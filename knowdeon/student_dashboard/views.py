from django.shortcuts import render
from student_dashboard.models import Course, Module, SubmitedCourse, Chapter, Section, Item
from django.contrib.auth.decorators import login_required
from knowdeon.forms import SignUpForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.http import HttpResponse

# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            # user.profile.phone_number = form.cleaned_data.get('phone_number')
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
    sections = Section.objects.select_related('chapter').filter(chapter_id=chapter.id).order_by('position')
    context = {'submited_course' : submited_course, 'chapter': chapter}
    if chapter.module.position == submited_course.current_module  and chapter.position == submited_course.current_chapter and not submited_course.completed:
        # this chapter is not completed yet
        sections = sections.filter(position__lte=submited_course.current_section)
        context['chapter_review'] = False

        # check what button to put at the bottom

        more_sections = Section.objects.select_related('chapter').filter(chapter_id=chapter.id, position__gt=submited_course.current_section)
        context['more_sections'] = more_sections
        if not more_sections:
            more_chapters = Chapter.objects.filter(
            module__course__submitedcourse__id=submited_course.id,
            module__position=submited_course.current_module,
            position__gt=submited_course.current_chapter,).order_by('position')
            context['more_chapters'] = more_chapters
            if not more_chapters:
                more_modules = Module.objects.filter(
                course__submitedcourse__id=submited_course.id,
                position__gt=submited_course.current_module,).order_by('position')
                context['more_modules'] = more_modules
                if not more_modules:
                    context['complete_course'] = True
    else:
        # this chapter was already viewed before
        context['chapter_review'] = True
        next_chapters = Chapter.objects.filter(module__id=chapter.module.id, position=chapter.position + 1).order_by('position')
        if next_chapters:
            context['next_chapter'] = next_chapters[0]
        else:
            next_modules = Module.objects.filter(id=chapter.module.id + 1).order_by('position')
            if next_modules:
                context['next_module'] = next_modules[0]
                next_chapters = Chapter.objects.filter(module__id=context['next_module'].id).order_by('position')
                context['next_chapter'] = next_chapters[0]
            else:
                
                context['end_course'] = True
                #end of the course
    context['sections'] = sections
    context['items'] = Item.objects.select_related('section').filter(section__chapter__id=kwargs['chapter_id']).order_by('position') #filter.(section__chapter__module__course_id=submited_course.course.id) 

    return render(request, 'student_dashboard/chapter.html', context)

def next_section(request):

    submited_course_id = request.POST.get('submited_course')

    submited_course = SubmitedCourse.objects.get(id=submited_course_id)
    
    if request.POST.get('next') == 'chapter':
        next_chapters = Chapter.objects.filter(module__course__submitedcourse__id=submited_course.id,
            module__position=submited_course.current_module,
            position__gt=submited_course.current_chapter,).order_by('position')
        submited_course.current_chapter += 1
        submited_course.current_section = 1
        submited_course.save()
    if request.POST.get('next') == 'module':
        submited_course.current_module += 1
        submited_course.current_chapter = 1
        submited_course.current_section = 1
        submited_course.save()
        next_chapters = Chapter.objects.filter(module__course__submitedcourse__id=submited_course.id,
            module__position=submited_course.current_module).order_by('position')
    if request.POST.get('next') == 'complete':
        submited_course.completed = True
        submited_course.save()
        return HttpResponse('http://' + request.get_host() + '/student_dashboard/course/' + str(submited_course_id) + '/')

    if request.POST.get('next') in ['chapter', 'module', 'complete']:

        if next_chapters:
            next_chapter_id = next_chapters[0].id
        return HttpResponse('http://' + request.get_host() + '/student_dashboard/chapter/' + str(submited_course_id) + '/' + str(next_chapter_id) + '/')

    more_sections = Section.objects.filter(
        chapter__module__course__submitedcourse__id=submited_course.id,
        chapter__module__position=submited_course.current_module,
        chapter__position=submited_course.current_chapter,
        position__gt=submited_course.current_section,).order_by('position')
    if len(more_sections) > 1:
        # next_section = more_sections.get(position=submited_course.current_section + 1)
        next_section = more_sections[0]
        submited_course.current_section += 1
        submited_course.save()
        items = Item.objects.filter(section__id=next_section.id).order_by('position')
        next_button = 'section'

        return render(request, 'student_dashboard/_section.html', {'submited_course' : submited_course ,'items' : items, 'next_button' : next_button })

    more_chapters = Chapter.objects.filter(
        module__course__submitedcourse__id=submited_course.id,
        module__position=submited_course.current_module,
        position__gt=submited_course.current_chapter,).order_by('position')
    
    if more_sections: #last one
        next_section = more_sections[0]
        
        items = Item.objects.filter(section__id=next_section.id).order_by('position')

    # no sections inserted for this chapter
    else:
        items = {}
            
    if more_chapters:
        # next_chapter = more_chapters.get(position=submited_course.current_chapter + 1)
        next_chapter = more_chapters[0]
        # move to next chapter
        #next chapter, first section
        submited_course.current_section += 1
        submited_course.save()
        next_button = 'chapter'

        return render(request, 'student_dashboard/_section.html', {'submited_course' : submited_course, 'items' : items, 'next_button' : next_button})

    more_modules = Module.objects.filter(
        course__submitedcourse__id=submited_course.id,
        position__gt=submited_course.current_module,).order_by('position')

    if more_modules:
        # next_module = more_modules.get(position=submited_course.current_module + 1)
        next_module = more_modules[0]
        submited_course.current_section += 1
        submited_course.save()
        next_button = 'module'

        return render(request, 'student_dashboard/_section.html', {'submited_course' : submited_course, 'items' : items, 'next_button' : next_button})

    else:
        submited_course.current_section += 1
        submited_course.save()
        next_button = 'complete_course'

        return render(request, 'student_dashboard/_section.html', {'submited_course' : submited_course, 'items' : items, 'next_button' : next_button})

def reset_progress(request, *args, **kwargs):
    submited_course = SubmitedCourse.objects.get(id=kwargs['submited_course'])
    submited_course.current_module = 1
    submited_course.current_chapter = 1
    submited_course.current_section = 1
    submited_course.completed = False
    submited_course.save()

    return redirect('/student_dashboard/course/' + str(submited_course.id) + '/')