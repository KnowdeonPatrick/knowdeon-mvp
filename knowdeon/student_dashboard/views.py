from django.shortcuts import render
from student_dashboard.models import Course, Module
# Create your views here.

def index(request):
    courses = Course.objects.all()
    return render(request, 'student_dashboard/index.html', {'courses': courses, 'card' : '<b>card</b>'})