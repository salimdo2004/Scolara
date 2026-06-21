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
]