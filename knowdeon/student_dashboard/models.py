from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
    background = models.TextField(max_length=2000, default='')
    address = models.CharField(max_length=256, default='')
    phone_number = models.CharField(max_length=20, default='')
    company = models.CharField(max_length=256, default='')
    industry = models.CharField(max_length=256, default='')
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Course(models.Model):
    course_name = models.CharField(max_length=256, default='')
    instructor = models.CharField(max_length=256, default='')
    expected_duration = models.IntegerField(default=0)
    date_reseased = models.DateTimeField(auto_now=False, auto_now_add=True)
    course_overview = models.TextField(max_length=2000, default='')
    is_active = models.BooleanField(default=True)

class Module(models.Model):
    module_name = models.CharField(max_length=256, default='')
    module_overview = models.TextField(max_length=2000, default='')
    is_active = models.BooleanField(default=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

class Section(models.Model):
    section_name = models.CharField(max_length=256, default='')
    section_text = models.TextField(max_length=2000, default='')
    video_link = models.CharField(max_length=256, default='') # path or url
    quiz = models.TextField(max_length=2000, default='') # embeded google forms
    images = models.TextField(max_length=2000, default='')
    module = models.ForeignKey(Module, on_delete=models.CASCADE)

class SubmitedCourse(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_submited = models.DateTimeField(auto_now=False, auto_now_add=True)
    is_active = models.BooleanField(default=True)
    current_module = models.IntegerField(default=0)
    current_section = models.IntegerField(default=0)
    video_paused_on = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_favourite = models.BooleanField(default=True)
    completed = models.BooleanField(default=True)