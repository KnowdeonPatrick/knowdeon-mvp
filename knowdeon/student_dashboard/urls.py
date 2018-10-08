from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', auth_views.login, {'template_name' : 'student_dashboard/login.html'}, name='login'),
    path('index/', views.index , name='index'),
]