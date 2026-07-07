from django.db import models
import datetime
# Create your models here.
from django.contrib.auth.hashers import make_password, check_password



class Parent(models.Model):
   
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    child_id = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    occupation = models.CharField(max_length=100)
    role = models.CharField(max_length=20)

    def __str__(self):
        return self.username


class Staff(models.Model):
    school = models.ForeignKey(
        'School',
        on_delete=models.CASCADE,
        related_name="staff_members"
    )

    employee_id = models.CharField(max_length=20, unique=True)

    full_name = models.CharField(max_length=200)

    role = models.CharField(
        max_length=50,
        choices=[
            ("SECRETARY", "Secrétaire"),
            ("Comptable", "Comptable"),
            ("SUPERVISOR", "Surveillant"),
            ("ADMIN", "Administrateur"),
        ]
    )

    email = models.EmailField()
    phone = models.CharField(max_length=20)

    password = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name
    

class Teacher(models.Model):

    school = models.ForeignKey(
        'School',
        on_delete=models.CASCADE,
        related_name="teachers"
    )

    teacher_id = models.CharField(
        max_length=20,
        unique=True
    )

    full_name = models.CharField(max_length=200)

    subject = models.CharField(max_length=100)

    email = models.EmailField()

    phone = models.CharField(max_length=20)

    password = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name
    

class School(models.Model):
    school_id = models.CharField(max_length=20, unique=True, blank=True)
    school_name = models.CharField(max_length=100)
    school_type = models.CharField(max_length=50)
    level = models.CharField(max_length=50)
    school_code = models.CharField(max_length=50, blank=True, null=True)
    year_created = models.DateField()

    address = models.TextField()
    region = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.school_id:
            last = School.objects.order_by('id').last()

            if last and last.school_id:
                num = int(last.school_id.replace("SCH", "")) + 1
            else:
                num = 1

            self.school_id = f"SCH{num:03d}"

        super().save(*args, **kwargs)


class Director(models.Model):
    director_id = models.CharField(max_length=20, unique=True, blank=True)

    school = models.OneToOneField(
        'School',
        on_delete=models.CASCADE,
        related_name='director'
    )

    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    password = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        if not self.director_id:
            last = Director.objects.order_by('id').last()

            if last and last.director_id:
                num = int(last.director_id.replace("DIR", "")) + 1
            else:
                num = 1

            self.director_id = f"DIR{num:03d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name

class Student(models.Model):

    # =========================
    # 🔹 CHOIX VILLES MAROC
    # =========================
    CITY_CHOICES = [
    ("RABAT", "Rabat"),
    ("CASABLANCA", "Casablanca"),
    ("FES", "Fès"),
    ("MARRAKECH", "Marrakech"),
    ("TANGER", "Tanger"),
    ("AGADIR", "Agadir"),
    ("MEKNES", "Meknès"),
    ("OUJDA", "Oujda"),
    ("KENITRA", "Kénitra"),
    ("TETOUAN", "Tétouan"),
    ]

    # =========================
    # 🔹 STATUS CHOICES
    # =========================
    STATUS_CHOICES = [
        ("active", "Active"),
        ("suspended", "Suspended"),
        ("graduated", "Graduated"),
        ("dropped", "Dropped"),
    ]


    COUNTRY_CHOICES = [

    ("Morocco","Morocco"),
    ("France","France"),
    ("Spain","Spain"),
    ("Portugal","Portugal"),
    ("Belgium","Belgium"),
    ("Germany","Germany"),
    ("Italy","Italy"),
    ("United Kingdom","United Kingdom"),
    ("Canada","Canada"),
    ("United States","United States"),
    ("Algeria","Algeria"),
    ("Tunisia","Tunisia"),
    ("Mauritania","Mauritania"),

]
    # =========================
    # 🔹 INFOS PERSONNELLES
    # =========================
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)

    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)

    date_of_birth = models.DateField(default=datetime.date(2000, 1, 1))
    place_of_birth = models.CharField(max_length=100, blank=True)

    address = models.TextField(blank=True)
    city = models.CharField(max_length=50, choices=CITY_CHOICES, default="RABAT")
    country = models.CharField(max_length=100,choices=COUNTRY_CHOICES,default="Morocco")

    # =========================
    # 🔹 IDENTIFIANT ETUDIANT
    # =========================
    student_id = models.CharField(max_length=50, unique=True, blank=True)

    # =========================
    # 🔹 INFO SCOLAIRE
    # =========================
    school = models.ForeignKey(
    School,
    on_delete=models.CASCADE,
    related_name="students"
)
    level = models.CharField(max_length=50)
    field_of_study = models.CharField(max_length=100)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="active"
    )

    enrollment_date = models.DateField(default=datetime.date.today)

    # =========================
    # 🔹 PARENT (PERE)
    # =========================
    parent_name_father = models.CharField(max_length=100)
    parent_phone_father = models.CharField(max_length=20)
    parent_email_father = models.EmailField(blank=True, null=True)
    parent_job_father = models.CharField(max_length=100, blank=True)

    # =========================
    # 🔹 PARENT (MERE)
    # =========================
    parent_name_mother = models.CharField(max_length=100)
    parent_phone_mother = models.CharField(max_length=20)
    parent_email_mother = models.EmailField(blank=True, null=True)
    parent_job_mother = models.CharField(max_length=100, blank=True)

    # =========================
    # 🔹 CONTACT URGENCE
    # =========================
    emergency_phone = models.CharField(max_length=20, blank=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    # =========================
    # 🔹 SYSTEM
    # =========================
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith("pbkdf2_"):
            self.password = make_password(self.password)

        if not self.student_id:
            city_code = (self.city or "UNK")[:3].upper()
            year = datetime.datetime.now().year

            prefix = f"{city_code}-{year}-"

            last_student = (
                Student.objects.filter(student_id__startswith=prefix)
                .order_by("-student_id")
                .first()
            )

            if last_student:
                last_number = int(last_student.student_id.split("-")[-1])
                new_number = last_number + 1
            else:
                new_number = 1

            self.student_id = f"{prefix}{new_number:04d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.student_id})"