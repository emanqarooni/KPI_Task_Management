from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import EmployeeKpi, ProgressEntry, Kpi
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# create your views here
def home(request):
    return render(request, 'home.html')
