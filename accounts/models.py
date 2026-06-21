from django.db import models

# Create your models here.




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


class Student(models.Model):
    student_id = models.CharField(max_length=50)
    password = models.CharField(max_length=255)


class Staff(models.Model):
    employee_id = models.CharField(max_length=50)
    school_code = models.CharField(max_length=50)
    password = models.CharField(max_length=255)

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

    director_name = models.CharField(max_length=100)
    director_email = models.EmailField()
    director_phone = models.CharField(max_length=20)
    director_password = models.CharField(max_length=255)

def save(self, *args, **kwargs):
    if not self.school_id:
        last = School.objects.all().order_by('id').last()
        if last and last.school_id:
            num = int(last.school_id.replace("SCH", "")) + 1
        else:
            num = 1

        self.school_id = f"SCH{num:03d}"

    super().save(*args, **kwargs)