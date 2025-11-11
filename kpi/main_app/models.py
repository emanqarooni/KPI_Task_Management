from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date

DEPARTMENT = (
    ("SM", "Sales & Marketing"),
    ("IT", "Information Technology"),
    ("HR", "Human Resources"),
    ("PM", "Project Management"),
)
# Create your models here.


class EmployeeProfile(models.Model):
    ROLE_CHOICES = [
        ("admin", "Admin"),
        ("manager", "Manager"),
        ("employee", "Employee"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    job_role = models.CharField(max_length=100)
    department = models.CharField(max_length=2, choices=DEPARTMENT)
    image = models.ImageField(upload_to="profile_images/", blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="employee")

    def __str__(self):
        return f"{self.user.username} - {self.job_role}"


class Kpi(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
<<<<<<< HEAD
    department = models.CharField(max_length=2, choices=DEPARTMENT, default=DEPARTMENT[0][0])
=======
    department = models.CharField(
        max_length=2, choices=DEPARTMENT, default=DEPARTMENT[0][0]
    )
>>>>>>> e3e1e1bebf33f8ce355522c3f130781de6d9f1b2
    # def __str__(self):
    #     return f"{self.plushie.name} {self.get_method_display()} on {self.date}"


class EmployeeKpi(models.Model):
    kpi = models.ForeignKey(Kpi, on_delete=models.CASCADE)
    target_value = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    weight = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

<<<<<<< HEAD
=======

>>>>>>> e3e1e1bebf33f8ce355522c3f130781de6d9f1b2
class ProgressEntry(models.Model):
    employee_kpi = models.ForeignKey(EmployeeKpi, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    note = models.TextField(max_length=250)
    date = models.DateField()

    def __str__(self):
        return self.name
