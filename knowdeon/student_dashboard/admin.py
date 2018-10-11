from django.contrib import admin
from student_dashboard.models import Course, Module, SubmitedCourse, Chapter, Section, Item
# Register your models here.

admin.site.register(SubmitedCourse)
admin.site.register(Course)
admin.site.register(Module)
admin.site.register(Chapter)
admin.site.register(Section)
admin.site.register(Item)