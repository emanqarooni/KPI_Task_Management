from django.shortcuts import render, redirect
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

def assign_kpi(request):
    # TEMP: Disable authentication & role check for testing
    if request.method == 'POST':
        form = AssignKpiForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "KPI successfully assigned.")
            return redirect('assign_kpi')
    else:
        form = AssignKpiForm()

    context = {'form': form}
    return render(request, 'main_app/assign_kpi.html', context)
