from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import EmployeeKpi, ProgressEntry, Kpi
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import EmployeeProfile
# EmployeeKpi

# Employee dashboard'
def dashboard(request):
    profile = EmployeeProfile.objects.get(user=request.user)

    if profile.role == "admin":
        return admin_dashboard(request)
    elif profile.role == "manager":
        return manager_dashboard(request)
    else:
        return employee_dashboard(request)


def admin_dashboard(request):
    total_users = User.objects.count()
    total_employees = EmployeeProfile.objects.filter(role="employee").count()

    context = {
        "total_users": total_users,
        "total_employees": total_employees,
    }
    return render(request, "dashboards/admin_dashboard.html", context)
    # kpis = EmployeeKpi.objects.all()
    # return render(request, "dashboards/admin_dashboard.html", {
    #     "profiles": profiles,
    #     "kpis": kpis,

def manager_dashboard(request):
    profile = EmployeeProfile.objects.get(user=request.user)
    department = profile.department

    employees_in_department = EmployeeProfile.objects.filter(department=department, role="employee").count()

    context = {
        "manager": profile,
        "department": profile.get_department_display(),
        "employees_count": employees_in_department,
    }
    return render(request, "dashboards/manager_dashboard.html", context)

    # team = profile.team_members.all()
    # team_kpis = EmployeeKpi.objects.filter(employee__in=team)
    # return render(request, "dashboards/manager_dashboard.html", {
    #     "profile": profile,
    #     "team": team,
    #     "team_kpis": team_kpis,
    # })

def employee_dashboard(request):
    profile = EmployeeProfile.objects.get(user=request.user)
    return render(request, "dashboards/employee_dashboard.html", {"profile": profile})

    # profile = EmployeeProfile.objects.get(user=request.user)
    # kpis = profile.assigned_kpis.select_related("kpi").all()
    # return render(request, "dashboards/employee_dashboard.html", {
    #     "profile": profile,
    #     "kpis": kpis,
    # })
# Manager Dashboard

# Admin Dashboard

# create your views here
def home(request):
    return render(request, "home.html")


def kpis_index(request):
    # kpi = Kpi.objects.get(id=kpi_id)

    return render(request, "kpi/detail.html")
