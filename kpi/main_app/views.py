from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse
from .models import EmployeeKpi, ProgressEntry, Kpi, EmployeeProfile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import AssignKpiForm, KpiProgressForm
from django.contrib import messages
from django.views.generic import CreateView, UpdateView, View


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
    if form.is_valid():
        form.save()
        return redirect('progress')
    return render(request, 'kpi/progress.html', {'form': form})


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

