from django.shortcuts import render
from student_dashboard.models import Course, Module, SubmitedCourse, Chapter, Section, Item
# Create your views here.

def index(request):
    
    user = request.user
    submited_courses = SubmitedCourse.objects.select_related('course').filter(user__id=user.id, is_active=True)

    recomended_courses = Course.objects.exclude(submitedcourse__user_id=user.id).filter(is_active=True)
    return render(request, 'student_dashboard/index.html', {'submited_courses': submited_courses, 'recomended_courses' : recomended_courses})

def course_view(request, *args, **kwargs):
    submited_course = SubmitedCourse.objects.select_related('course').get(id=kwargs['pk'])
    modules = Module.objects.filter(course_id=submited_course.course.id).order_by('position')
    chapters = Chapter.objects.select_related('module').filter(module__course_id=submited_course.course.id).order_by('module__position', 'position')
    return render(request, 'student_dashboard/course.html', {'submited_course' : submited_course, 'modules' : modules, 'chapters' : chapters})

def chapter_view(request, *args, **kwargs):
    submited_course = SubmitedCourse.objects.select_related('course').get(id=kwargs['submited_course'])
    chapter = Chapter.objects.get(id=kwargs['chapter_id'])
    sections = Section.objects.select_related('chapter').filter(chapter_id=chapter.id, position__lte=submited_course.current_section)#.filter(chapter__module__course_id=submited_course.course.id)

    items = Item.objects.select_related('section').filter(section__chapter__module__course_id=submited_course.course.id, section__chapter__id=kwargs['chapter_id'])

    return render(request, 'student_dashboard/chapter.html', { 'submited_course' : submited_course,'chapter': chapter, 'sections': sections,'items': items})

def next_section(request):
    print(request.POST.get('current_section'))
    current_section_id = request.POST.get('current_section')
    current_chapter_id = request.POST.get('current_chapter')
    # change current point + 1
    # get next section
    return render(request, 'student_dashboard/index.html')