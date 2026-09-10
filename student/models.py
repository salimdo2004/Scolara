from django.db import models

# Create your models here.

class Notification(models.Model):

    ROLE_CHOICES = [
        ("director", "Directeur"),
        ("student", "Étudiant"),
        ("staff", "Personnel"),
        ("teacher", "Professeur"),
        ("parent", "Parent"),
    ]

    user_id = models.PositiveIntegerField()

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="director"
    )

    title = models.CharField(max_length=255)
    message = models.TextField()

    icon = models.CharField(
        max_length=100,
        default="fa-bell"
    )

    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.role} #{self.user_id} - {self.title}"