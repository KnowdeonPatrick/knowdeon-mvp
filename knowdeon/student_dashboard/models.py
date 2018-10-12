from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class Profile(models.Model):
    background = models.TextField(max_length=2000, default='')
    address = models.CharField(max_length=256, default='')
    phone_number = models.CharField(max_length=20, default='')
    company = models.CharField(max_length=256, default='')
    industry = models.CharField(max_length=256, default='')
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    @receiver(post_save, sender=User)
    def update_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save() 


class Course(models.Model):
    course_name = models.CharField(max_length=256, default='')
    instructor = models.CharField(max_length=256, default='')
    expected_duration = models.IntegerField(default=0)
    date_reseased = models.DateTimeField(auto_now=False, auto_now_add=True)
    course_overview = models.TextField(max_length=2000, default='')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.course_name

class Module(models.Model):
    module_name = models.CharField(max_length=256, default='')
    position = models.IntegerField(default=0)
    module_overview = models.TextField(max_length=2000, default='')
    is_active = models.BooleanField(default=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.module_name

class Chapter(models.Model):
    chapter_name = models.CharField(max_length=256, default='')
    chapter_overview = models.TextField(max_length=2000, default='')
    position = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)

    def __str__(self):
        return self.chapter_name

class Section(models.Model):
    section_name = models.CharField(max_length=256, default='')
    section_overview = models.TextField(max_length=2000, default='')
    position = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)

    def __str__(self):
        return self.section_name

class Item(models.Model):
    item_name = models.CharField(max_length=256, default='')
    position = models.IntegerField(default=0)
    item_text = models.TextField(max_length=2000, default='null')
    video_link = models.CharField(max_length=256, default='null') # path or url
    quiz = models.TextField(max_length=2000, default='null') # embeded google forms
    image = models.TextField(max_length=2000, default='null')
    section = models.ForeignKey(Section, on_delete=models.CASCADE)

class SubmitedCourse(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_submited = models.DateTimeField(auto_now=False, auto_now_add=True)
    is_active = models.BooleanField(default=True)
    current_module = models.IntegerField(default=1)
    current_chapter = models.IntegerField(default=1)
    current_section = models.IntegerField(default=1)
    video_paused_on = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_favourite = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)