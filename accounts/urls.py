from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="home"),

    path("create-school/", views.create_school, name="create_school"),

    path("register/", views.register, name="register"),
    path(
        "student/register/",
        views.student_form,
        name="student_form"
    ),
path(
    "student/login/",
    views.student_login,
    name="student_login"
),

path(
    "student/dashboard/",
    views.student_dashboard,
    name="student_dashboard"
),
    # Connexions
    path("login/", views.login_view, name="login"),
    path("login/student/", views.student_login, name="student_login"),
    path("login/parent/", views.parent_login, name="parent_login"),
    path("login/staff/", views.staff_login, name="staff_login"),

    # Profil
    path("profile/", views.profile, name="profile"),
    path("logout/", views.logout_view, name="logout"),

    # École
    path(
        "school/<int:school_id>/director/",
        views.school_director,
        name="school_director"
    ),

    path(
        "school/<int:school_id>/staff/",
        views.create_staff,
        name="create_staff"
    ),

    path(
        "school/<int:school_id>/teacher/",
        views.create_teacher,
        name="create_teacher"
    ),

    path(
        "school/<int:school_id>/create_student/",
        views.student_create,
        name="student_form"
    ),

    # AJAX
    path(
        "get-schools/",
        views.get_schools,
        name="get_schools"
    ),


]