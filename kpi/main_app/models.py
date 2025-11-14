from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date
from django.db.models import Sum

DEPARTMENT = (
    ("SM", "Sales & Marketing"),
    ("IT", "Information Technology"),
    ("HR", "Human Resources"),
    ("PM", "Project Management"),
)

GENDER = (
    ("M", "Male"),
    ("F", "Female"),
)

# Create your models here.


class EmployeeProfile(models.Model):
    ROLE_CHOICES = [
        ("admin", "Admin"),
        ("manager", "Manager"),
        ("employee", "Employee"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=1, choices=GENDER, default="M")
    job_role = models.CharField(max_length=100)
    department = models.CharField(
        max_length=2, choices=DEPARTMENT, default=DEPARTMENT[0][0]
    )
    image = models.ImageField(upload_to="profile_images/", blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="employee")

    manager = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="managed_employees",
    )

    def save(self, *args, **kwargs):
        # automatically assign admin role to superusers
        if self.user.is_superuser:
            self.role = "admin"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.job_role}"


class Kpi(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    department = models.CharField(
        max_length=2, choices=DEPARTMENT, default=DEPARTMENT[0][0]
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("detail", kwargs={"kpi_id": self.id})


class EmployeeKpi(models.Model):
    employee = models.ForeignKey(EmployeeProfile, on_delete=models.CASCADE)
    kpi = models.ForeignKey(Kpi, on_delete=models.CASCADE)
    target_value = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    weight = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.employee.user.username} - {self.kpi.title} ({self.weight}%)"

    # in views for dashboard
    #     def current_progress(self):
    #         total = sum(entry.value for entry in self.progressentry_set.all())
    #         return total
    #     def progress_percentage(self):
    #         if self.target_value == 0:
    #             return 0
    #         return (self.current_progress() / self.target_value) * 100
    #     def days_left(self):
    #         return (self.end_date - date.today()).days

    # func for counting the total progress entries that the employees add
    def total_progress(self):
        agg = self.progressentry_set.aggregate(total=Sum("value"))
        return agg["total"] or 0

    # func for returining the num of each progress entries added by employees
    def progress_count(self):
        return self.progressentry_set.count()


    # func to calculate and return the percentage of completion
    def progress_percentage(self):
        total = self.total_progress()
        if self.target_value == 0:
            return 0
        percentage = (total / self.target_value) * 100
        return round(percentage)

    # func for status: so if the total entries is 0 then no progress, and if the total entires is more than zero then and if the target value reach the total then the status will be complete
    def status(self):
        total = self.total_progress()
        if total == 0:
            return "No Progress"
        if total == self.target_value:
            return "Complete"
        return "In Progress"


class ProgressEntry(models.Model):
    employee_kpi = models.ForeignKey(EmployeeKpi, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    note = models.TextField(max_length=250)
    date = models.DateField()



    def __str__(self):
        return f"{self.employee_kpi.employee.user.username} - {self.value}"
