from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpResponse
from .models import EmployeeKpi, ProgressEntry, Kpi, EmployeeProfile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import AssignKpiForm, KpiProgressForm
from django.contrib import messages
from django.views.generic import CreateView, UpdateView, View
from django.contrib import messages

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
    kpis = Kpi.objects.all()
    return render(request, "kpi/index.html", {"kpis": kpis})


def kpis_detail(request, kpi_id):
    kpi = Kpi.objects.get(id=kpi_id)
    return render(request, "kpi/detail.html", {"kpi": kpi})


def add_progress(request):
    form = KpiProgressForm()

    employee_kpi_id = request.POST.get('employee_kpi')
    if employee_kpi_id:
        employee_kpi = EmployeeKpi.objects.get(id=employee_kpi_id)
        if employee_kpi.status() == "Complete":
            messages.warning(request, "This KPI is already complete. You cannot add more progress.")
            return redirect('progress')
    if form.is_valid():
            form.save()
            messages.success(request, "Progress added successfully!")
            return redirect('progress')

    return render(request, 'kpi/progress.html', {'form': form})



def employee_kpi(request):
     employee_kpi = EmployeeKpi.objects.all()
     return render(request, "kpi/employee_kpi.html", {"employee_kpi": employee_kpi})



class KpiCreate(CreateView):
    model = Kpi
    fields = "__all__"
    success_url = "/kpis/"


class KpiUpdate(UpdateView):
    model = Kpi
    fields = "__all__"


# manager: assign kpi
# # @login_required
# def assign_kpi(request):
#     # Only managers can assign KPI
#     if not request.user.employeeprofile.role in ['manager']:
#         messages.error(request, "You are not authorized to assign KPIs.")
#         return redirect('home')

#     if request.method == 'POST':
#         form = AssignKpiForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "KPI successfully assigned to employee.")
#             return redirect('assign_kpi')
#     else:
#         form = AssignKpiForm()

#     context = {
#         'form': form,
#         'user': request.user
#     }
#     return render(request, 'main_app/assign_kpi.html', context)

# Assign KPI: managers assign employees to KPI; KPIs & employees filtered by manager's department
def assign_kpi(request):
    # pass request.user into the form so it filters by department if user is manager
    form = AssignKpiForm(request.POST or None, user=(request.user if request.user.is_authenticated else None))
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "KPI assigned successfully.")
            return redirect('employee_kpi_list')
    return render(request, 'main_app/assign_kpi.html', {'form': form})

def employee_kpi_list(request):
    if request.user.is_authenticated and hasattr(request.user, "employeeprofile") and request.user.employeeprofile.role == "manager":
        dept = request.user.employeeprofile.department
        # show only assignments where employee is in manager's department
        kpis = EmployeeKpi.objects.filter(employee__department=dept).select_related('employee__user', 'kpi')
    else:
        kpis = EmployeeKpi.objects.select_related('employee__user', 'kpi').all()
    return render(request, 'main_app/employee_kpi_list.html', {'kpis': kpis})

def employee_kpi_edit(request, pk):
    kpi_assign = get_object_or_404(EmployeeKpi, pk=pk)
    if kpi_assign.progressentry_set.exists():
        messages.error(request, "Cannot edit KPI — progress already exists.")
        return redirect('employee_kpi_list')

    form = AssignKpiForm(request.POST or None, instance=kpi_assign, user=(request.user if request.user.is_authenticated else None))
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "KPI updated successfully.")
        return redirect('employee_kpi_list')

    return render(request, 'main_app/employee_kpi_edit.html', {'form': form, 'kpi': kpi_assign})

def employee_kpi_delete(request, pk):
    kpi_assign = get_object_or_404(EmployeeKpi, pk=pk)
    if kpi_assign.progressentry_set.exists():
        messages.error(request, "Cannot delete KPI — progress already exists.")
        return redirect('employee_kpi_list')

    if request.method == 'POST':
        kpi_assign.delete()
        messages.success(request, "KPI assignment deleted.")
        return redirect('employee_kpi_list')

    return render(request, 'main_app/employee_kpi_delete.html', {'kpi': kpi_assign})

def employee_kpi_detail(request, pk):
    kpi_assign = get_object_or_404(EmployeeKpi, pk=pk)
    progress_entries = kpi_assign.progressentry_set.order_by('date')
    return render(request, 'main_app/employee_kpi_detail.html', {
        'kpi': kpi_assign,
        'progress_entries': progress_entries,
    })

