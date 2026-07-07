from django.urls import path
from .views import *

from . import views



urlpatterns = [
    path('', views.index, name='home'),
    path('create-school/', views.create_school, name='create_school'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    path('school/<int:school_id>/director/',views.school_director,name='school_director'),
    path('school/<int:school_id>/staff/',views.create_staff,name='create_staff'),
    path('school/<int:school_id>/teacher/',views.create_teacher,name='create_teacher'),
    path('school/<int:school_id>/create_student/',views.student_create, name="student_form"),
    path("get-schools/",views.get_schools,name="get_schools"),
]
