from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', auth_views.login, {'template_name' : 'student_dashboard/login.html'}, name='login'),
    path('index/', views.index , name='index'),
    path('course/<int:pk>/', views.course_view, name="course_view"),
    path('chapter/<int:submited_course>/<int:chapter_id>/', views.chapter_view, name="chapter_view"),
    path('next-section/', views.next_section, name="next_section"),
    path('logout/', auth_views.logout, {'template_name' : 'student_dashboard/logout.html'}, name="logout" ),
    path('signup/', views.signup, name='signup'),
    path('reset_progress/<int:submited_course>/', views.reset_progress, name="reset_progress"),
]