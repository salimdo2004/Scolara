from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse

from .models import Notification
from accounts.models import Student


def dashboard(request):

    if request.session.get("user_role") != "student":
        return redirect("login")

    student_id = request.session.get("user_id")

    if not student_id:
        return redirect("login")

    student = get_object_or_404(Student, id=student_id)

    notifications = Notification.objects.filter(
        user_id=student.id,
        role="student"
    ).order_by("-created_at")

    unread_count = notifications.filter(
        is_read=False
    ).count()

    print("================================")
    print("ÉTUDIANT :", student.student_id)
    print("ID :", student.id)
    print("NOTIFICATIONS :", notifications.count())
    print("NON LUES :", unread_count)
    print("================================")

    return render(request, "student/index.html", {
        "user": student,
        "student": student,
        "role": "student",
        "notifications": notifications,
        "unread_count": unread_count,
    })


def mark_notification_read(request, notification_id):

    if request.session.get("user_role") != "student":
        return JsonResponse({
            "success": False
        }, status=403)

    student_id = request.session.get("user_id")

    notification = get_object_or_404(
        Notification,
        id=notification_id,
        user_id=student_id,
        role="student"
    )

    notification.is_read = True
    notification.save()

    return JsonResponse({
        "success": True
    })