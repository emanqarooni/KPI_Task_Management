from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse
from .models import EmployeeKpi, ProgressEntry, Kpi, EmployeeProfile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import AssignKpiForm
from django.contrib import messages

# create your views here
def home(request):
    return render(request, "home.html")

def kpis_index(request):
    # kpi = Kpi.objects.get(id=kpi_id)

    return render(request, "kpi/detail.html")

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

