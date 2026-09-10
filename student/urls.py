from django.urls import path
from .views import *

from . import views



urlpatterns = [
    path(
        "",
        views.dashboard,
        name="student_dashboard"
    ),

    path(
        "notifications/<int:notification_id>/read/",
        views.mark_notification_read,
        name="mark_notification_read"
    ),
]
