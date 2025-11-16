from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse
from .models import EmployeeKpi, ProgressEntry, Kpi, EmployeeProfile, ActivityLog
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, View
from .forms import AssignKpiForm, KpiProgressForm
from django.contrib import messages
from .decorators import RoleRequiredMixin, role_required
from django.contrib.auth.models import User
from django.db.models import Q

from .utils import log_activity
from django.contrib.admin.views.decorators import staff_member_required


# Employee dashboard'
def dashboard(request):
    # return render(request, "dashboards/dashboard_home.html")
    profile = EmployeeProfile.objects.get(user=request.user)

    if profile.role == "admin":
        return admin_dashboard(request)
    elif profile.role == "manager":
        return manager_dashboard(request)
    else:
        return employee_dashboard(request)


def admin_dashboard(request):
    from .models import ActivityLog

    total_users = User.objects.count()
    total_employees = EmployeeProfile.objects.filter(role="employee").count()

    # Add recent activity logs
    recent_logs = ActivityLog.objects.select_related('user', 'related_user')[:10]

    context = {
        "total_users": total_users,
        "total_employees": total_employees,
        "recent_logs": recent_logs,
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


@login_required
@role_required(['admin'])
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



@login_required
@role_required(['employee'])
def add_progress(request):
    if request.method == 'POST':
        form = KpiProgressForm(request.POST, user=request.user)

        if form.is_valid():
            employee_kpi = form.cleaned_data['employee_kpi']

            if employee_kpi.status() == "Complete":
                messages.error(request, "This KPI is already complete. You cannot add more progress.")
                return redirect('employee_kpi')


            progress = form.save()

            log_activity(
                user=request.user,
                action='PROGRESS_ADDED',
                description=f"Added progress for '{progress.employee_kpi.kpi.title}' - Value: {progress.value}",
                related_user=None
            )
            messages.success(request, "Progress added successfully!")
            return redirect('employee_kpi')

    else:
        form = KpiProgressForm(user=request.user)

    return render(request, 'kpi/progress.html', {'form': form})



@login_required
@role_required(['employee'])
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

# Assign KPI: managers assign employees to KPI; KPIs & employees filtered by manager's department
@login_required
@role_required(['manager'])
def assign_kpi(request):
    # pass request.user into the form so it filters by department if user is manager
    form = AssignKpiForm(
        request.POST or None,
        user=(request.user if request.user.is_authenticated else None),
    )
    if request.method == "POST":
        if form.is_valid():
            kpi_assignment=form.save()

            log_activity(
                user=request.user,
                action='KPI_ASSIGNED',
                description=f"Assigned '{kpi_assignment.kpi.title}' to {kpi_assignment.employee.user.username} (Target: {kpi_assignment.target_value}, Weight: {kpi_assignment.weight}%)",
                related_user=kpi_assignment.employee.user
            )

            messages.success(request, "KPI assigned successfully.")
            return redirect("employee_kpi_list")
    return render(request, "main_app/assign_kpi.html", {"form": form})

@login_required
@role_required(['manager'])
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
        ).order_by('-id')
    else:
        kpis = EmployeeKpi.objects.select_related("employee__user", "kpi").all()

    # search functionality
    search_query = request.GET.get('search', '').strip()
    if search_query:
        kpis = kpis.filter(
            Q(employee__user__username__icontains=search_query) |
            Q(employee__user__first_name__icontains=search_query) |
            Q(employee__user__last_name__icontains=search_query) |
            Q(employee__job_role__icontains=search_query)
        )

    # filter by KPI
    kpi_filter = request.GET.get('kpi', '')
    if kpi_filter:
        kpis = kpis.filter(kpi__id=kpi_filter)

    # order by newest first
    kpis = kpis.order_by('-id')

    status_filter = request.GET.get('status', '')
    if status_filter:
        # convert the queryset to a list and filter by status since status is a method
        filtered_kpis = []
        for kpi in kpis:
            kpi_status = kpi.status().lower().replace(' ', '_')
            if kpi_status == status_filter:
                filtered_kpis.append(kpi)
        kpis = filtered_kpis
    else:
        # convert to list for consistency
        kpis = list(kpis)

    # get all KPIs for the filter dropdown
    if (
        request.user.is_authenticated
        and hasattr(request.user, "employeeprofile")
        and request.user.employeeprofile.role == "manager"
    ):
        dept = request.user.employeeprofile.department
        all_kpis = Kpi.objects.filter(department=dept)
    else:
        all_kpis = Kpi.objects.all()

    context = {
        'kpis': kpis,
        'all_kpis': all_kpis,
        'search_query': search_query,
        'kpi_filter': kpi_filter,
        'status_filter': status_filter,
    }
    return render(request, "main_app/employee_kpi_list.html", context)

@login_required
@role_required(['manager'])
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
        kpi_assignment = form.save()

        log_activity(
            user=request.user,
            action='KPI_UPDATED',
            description=f"Updated KPI '{kpi_assignment.kpi.title}' for {kpi_assignment.employee.user.username}",
            related_user=kpi_assignment.employee.user
        )

        messages.success(request, "KPI updated successfully.")
        return redirect("employee_kpi_list")

    return render(
        request, "main_app/employee_kpi_edit.html", {"form": form, "kpi": kpi_assign}
    )

@login_required
@role_required(['manager'])
def employee_kpi_delete(request, pk):
    kpi_assign = get_object_or_404(EmployeeKpi, pk=pk)
    if kpi_assign.progressentry_set.exists():
        messages.error(request, "Cannot delete KPI — progress already exists.")
        return redirect("employee_kpi_list")

    if request.method == "POST":
        employee_name = kpi_assign.employee.user.username
        kpi_title = kpi_assign.kpi.title
        related_user = kpi_assign.employee.user

        log_activity(
            user=request.user,
            action='KPI_DELETED',
            description=f"Deleted KPI assignment '{kpi_title}' from {employee_name}",
            related_user=related_user
        )

        kpi_assign.delete()
        messages.success(request, "KPI assignment deleted.")
        return redirect("employee_kpi_list")

    return render(request, "main_app/employee_kpi_delete.html", {"kpi": kpi_assign})

@login_required
@role_required(['manager'])
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


@role_required(['admin'])
def activity_logs(request):
    # get url values form filter form
    selected_action = request.GET.get('action', '')
    selected_user = request.GET.get('user', '')

    all_logs = ActivityLog.objects.all()
    all_logs = all_logs.select_related('user', 'related_user')


    if selected_action:
        all_logs = all_logs.filter(action=selected_action)

    if selected_user:
        all_logs = all_logs.filter(user__username=selected_user)

    recent_logs = all_logs[:50]

    action_choices = ActivityLog.ACTION_CHOICES

    users_with_logs = User.objects.filter(activity_logs__isnull=False)
    users_with_logs = users_with_logs.select_related('employeeprofile')
    users_with_logs = users_with_logs.distinct()
    users_with_logs = users_with_logs.order_by('username')



    template_data = {
        'logs': recent_logs,
        'available_actions': action_choices,
        'active_users': users_with_logs,
        'current_action_filter': selected_action,
        'current_user_filter': selected_user,
    }
    return render(request, 'activity/admin_logs.html', template_data)
