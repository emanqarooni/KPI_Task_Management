from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import EmployeeKpi, ProgressEntry, Kpi
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# create your views here
def home(request):
    return render(request, 'home.html')



def kpis_index(request):
    # kpi = Kpi.objects.get(id=kpi_id)
    return render(request, "kpi/detail.html")
