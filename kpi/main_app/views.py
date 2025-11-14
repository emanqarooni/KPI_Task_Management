from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse
from .models import EmployeeKpi, ProgressEntry, Kpi, EmployeeProfile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, View
from .forms import AssignKpiForm, KpiProgressForm
from django.contrib import messages
from .decorators import RoleRequiredMixin, role_required
from django.contrib.auth.models import User
from django.db.models import Sum

# Employee dashboard'
@login_required
def dashboard(request):
    employee_profile = EmployeeProfile.objects.get(user=request.user)

    if employee_profile.role == "admin":
        return redirect("admin_dashboard")
    elif employee_profile.role == "manager":
        return redirect("manager_dashboard")
    else:
        return redirect("employee_dashboard")


# Admin dashboard
@login_required
@role_required(["admin"])
def admin_dashboard(request):
    total_users_count = User.objects.count()
    total_employees_count = EmployeeProfile.objects.filter(role="employee").count()

    all_kpis = Kpi.objects.all()

    chart_labels_list = []
    chart_values_list = []

    # Prepare ChartJS data
    for kpi in all_kpis:
        chart_labels_list.append(kpi.title)

        total_progress_for_kpi = 0
        employee_kpis_for_this_kpi = EmployeeKpi.objects.filter(kpi=kpi)

        for employee_kpi in employee_kpis_for_this_kpi:
            progress_entries = ProgressEntry.objects.filter(employee_kpi=employee_kpi)
            for progress_entry in progress_entries:
                total_progress_for_kpi += progress_entry.value

        chart_values_list.append(total_progress_for_kpi)

    context = {
        "total_users": total_users_count,
        "total_employees": total_employees_count,
        "kpis": all_kpis,
        "chart_labels": chart_labels_list,
        "chart_values": chart_values_list,
    }

    return render(request, "dashboards/admin_dashboard.html", context)


# Manager dashboard
@login_required
@role_required(["manager"])
def manager_dashboard(request):
    manager_profile = EmployeeProfile.objects.get(user=request.user)
    manager_department = manager_profile.department

    employees_in_department = EmployeeProfile.objects.filter(
        department=manager_department,
        role="employee"
    )

    employee_dashboard_rows = []

    # Loop through each employee
    for employee in employees_in_department:
        employee_kpis = EmployeeKpi.objects.filter(employee=employee)

        if employee_kpis.exists():
            total_progress_value = 0
            total_target_value = 0

            # Sum progress and target for all KPIs
            for employee_kpi in employee_kpis:
                progress_entries = employee_kpi.progressentry_set.all()
                for entry in progress_entries:
                    total_progress_value += entry.value

                total_target_value += employee_kpi.target_value

            if total_target_value == 0:
                completion_percentage = 0
            else:
                completion_percentage = round((total_progress_value / total_target_value) * 100)

            if completion_percentage == 0:
                status_text = "No Progress"
            elif completion_percentage >= 100:
                status_text = "Complete"
            else:
                status_text = "Moderate"

        else:
            completion_percentage = 0
            status_text = "No KPI Assigned"

        employee_dashboard_rows.append({
            "name": employee.user.username,
            "completion": completion_percentage,
            "status": status_text,
        })

    context = {
        "manager_name": manager_profile.user.username,
        "department": manager_profile.get_department_display(),
        "employees_count": employees_in_department.count(),
        "employee_rows": employee_dashboard_rows,
    }

    return render(request, "dashboards/manager_dashboard.html", context)


# Employee dashboard
@login_required
@role_required(["employee"])
def employee_dashboard(request):
    employee_profile = EmployeeProfile.objects.get(user=request.user)
    assigned_kpis = EmployeeKpi.objects.filter(employee=employee_profile)

    chart_labels_list = []
    chart_values_list = []
    kpi_cards_list = []

    # Loop through each assigned KPI
    for employee_kpi in assigned_kpis:
        kpi_title = employee_kpi.kpi.title
        total_progress_value = 0

        progress_entries = employee_kpi.progressentry_set.all()
        for entry in progress_entries:
            total_progress_value += entry.value

        if employee_kpi.target_value == 0:
            progress_percentage = 0
        else:
            progress_percentage = round((total_progress_value / employee_kpi.target_value) * 100)

        days_remaining = (employee_kpi.end_date - date.today()).days

        chart_labels_list.append(kpi_title)
        chart_values_list.append(progress_percentage)

        kpi_cards_list.append({
            "title": kpi_title,
            "target": employee_kpi.target_value,
            "progress": total_progress_value,
            "percentage": progress_percentage,
            "days_left": days_remaining,
            "id": employee_kpi.id,
        })

    context = {
        "employee_name": employee_profile.user.username,
        "role": employee_profile.job_role,
        "kpi_cards": kpi_cards_list,
        "chart_labels": chart_labels_list,
        "chart_values": chart_values_list,
    }

    return render(request, "dashboards/employee_dashboard.html", context)


# Manager Dashboard

# Admin Dashboard


# create your views here
def home(request):
    return render(request, "home.html")


@login_required
def kpis_index(request):
    kpis = Kpi.objects.all()
    return render(request, "kpi/index.html", {"kpis": kpis})


@login_required
def kpis_detail(request, kpi_id):
    kpi = Kpi.objects.get(id=kpi_id)
    return render(request, "kpi/detail.html", {"kpi": kpi})


class KpiCreate(RoleRequiredMixin, CreateView):
    model = Kpi
    fields = "__all__"
    success_url = "/kpis/"
    allowed_roles = ["admin"]


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
        return redirect('progress')
    return render(request, 'kpi/progress.html', {'form': form})



def employee_kpi(request):
    employee_kpi = EmployeeKpi.objects.all()
    return render(request, "kpi/employee_kpi.html", {"employee_kpi": employee_kpi})


class KpiUpdate(RoleRequiredMixin, UpdateView):
    model = Kpi
    fields = "__all__"
    allowed_roles = ["admin"]


# unauthorized access page
def unauthorized(request):
    return render(request, "unauthorized.html")


@login_required
def profile(request):
    return render(request, "users/profile.html")


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
    form = AssignKpiForm(
        request.POST or None,
        user=(request.user if request.user.is_authenticated else None),
    )
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "KPI assigned successfully.")
            return redirect("employee_kpi_list")
    return render(request, "main_app/assign_kpi.html", {"form": form})


def employee_kpi_list(request):
    if (
        request.user.is_authenticated
        and hasattr(request.user, "employeeprofile")
        and request.user.employeeprofile.role == "manager"
    ):
        dept = request.user.employeeprofile.department
        # show only assignments where employee is in manager's department
        kpis = EmployeeKpi.objects.filter(employee__department=dept).select_related(
            "employee__user", "kpi"
        )
    else:
        kpis = EmployeeKpi.objects.select_related("employee__user", "kpi").all()
    return render(request, "main_app/employee_kpi_list.html", {"kpis": kpis})


def employee_kpi_edit(request, pk):
    kpi_assign = get_object_or_404(EmployeeKpi, pk=pk)
    if kpi_assign.progressentry_set.exists():
        messages.error(request, "Cannot edit KPI — progress already exists.")
        return redirect("employee_kpi_list")

    form = AssignKpiForm(
        request.POST or None,
        instance=kpi_assign,
        user=(request.user if request.user.is_authenticated else None),
    )
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "KPI updated successfully.")
        return redirect("employee_kpi_list")

    return render(
        request, "main_app/employee_kpi_edit.html", {"form": form, "kpi": kpi_assign}
    )


def employee_kpi_delete(request, pk):
    kpi_assign = get_object_or_404(EmployeeKpi, pk=pk)
    if kpi_assign.progressentry_set.exists():
        messages.error(request, "Cannot delete KPI — progress already exists.")
        return redirect("employee_kpi_list")

    if request.method == "POST":
        kpi_assign.delete()
        messages.success(request, "KPI assignment deleted.")
        return redirect("employee_kpi_list")

    return render(request, "main_app/employee_kpi_delete.html", {"kpi": kpi_assign})


def employee_kpi_detail(request, pk):
    kpi_assign = get_object_or_404(EmployeeKpi, pk=pk)
    progress_entries = kpi_assign.progressentry_set.order_by("date")
    return render(
        request,
        "main_app/employee_kpi_detail.html",
        {
            "kpi": kpi_assign,
            "progress_entries": progress_entries,
        },
    )
