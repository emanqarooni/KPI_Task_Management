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
    return render(request, "dashboards/dashboard_home.html")
    # profile = EmployeeProfile.objects.get(user=request.user)

    # if profile.role == "admin":
    #     return admin_dashboard(request)
    # elif profile.role == "manager":
    #     return manager_dashboard(request)
    # else:
    #     return employee_dashboard(request)


def admin_dashboard(request):
    total_users = 8
    total_employees = 5

    context = {
        "total_users": total_users,
        "total_employees": total_employees,
    }
    return render(request, "dashboards/admin_dashboard.html", context)
    # total_users = User.objects.count()
    # total_employees = EmployeeProfile.objects.filter(role="employee").count()

    # context = {
    #     "total_users": total_users,
    #     "total_employees": total_employees,
    # }
    # kpis = EmployeeKpi.objects.all()
    # return render(request, "dashboards/admin_dashboard.html", {
    #     "profiles": profiles,
    #     "kpis": kpis,

def manager_dashboard(request):
    manager_name = "Shooq"
    department = "Information Technology"
    employees_count = 3

    context = {
        "manager_name": manager_name,
        "department": department,
        "employees_count": employees_count,
    }
    return render(request, "dashboards/manager_dashboard.html", context)
    # profile = EmployeeProfile.objects.get(user=request.user)
    # department = profile.department

    # employees_in_department = EmployeeProfile.objects.filter(department=department, role="employee").count()

    # context = {
    #     "manager": profile,
    #     "department": profile.get_department_display(),
    #     "employees_count": employees_in_department,
    # }

    # team = profile.team_members.all()
    # team_kpis = EmployeeKpi.objects.filter(employee__in=team)
    # return render(request, "dashboards/manager_dashboard.html", {
    #     "profile": profile,
    #     "team": team,
    #     "team_kpis": team_kpis,
    # })

def employee_dashboard(request):
    employee_name = "Maryam"
    department = "Sales & Marketing"
    role = "Employee"

    context = {
        "employee_name": employee_name,
        "department": department,
        "role": role,
    }
    return render(request, "dashboards/employee_dashboard.html", context)

    # profile = EmployeeProfile.objects.get(user=request.user)
    # return render(request, "dashboards/employee_dashboard.html", {"profile": profile})

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
