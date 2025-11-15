from django.contrib import admin
from .models import EmployeeProfile, Kpi, EmployeeKpi, ProgressEntry
from django.contrib.auth.models import User
from django import forms


# adding custom form to hide the Admin option
class EmployeeProfileForm(forms.ModelForm):
    class Meta:
        model = EmployeeProfile
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(EmployeeProfileForm, self).__init__(*args, **kwargs)
        # removing admin role from dropdown because no need another admin user
        role_choices = [
            choice for choice in self.fields["role"].choices if choice[0] != "admin"
        ]
        self.fields["role"].choices = role_choices


# register EmployeeProfile with custom form that have admin role removed from the options
@admin.register(EmployeeProfile)
class EmployeeProfileAdmin(admin.ModelAdmin):
    form = EmployeeProfileForm

    list_display = ("user", "job_role", "department", "role", "manager")
    list_filter = ("department", "role")
    search_fields = ("user__username", "job_role")

    # since manager is foreignkey , this function manages the filter of only "managers" in the dropdown and not all users.
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "manager":
            kwargs["queryset"] = User.objects.filter(employeeprofile__role="manager")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# Register your models here.
admin.site.register(Kpi)
admin.site.register(EmployeeKpi)
admin.site.register(ProgressEntry)
