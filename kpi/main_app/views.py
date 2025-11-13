from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import EmployeeKpi, EmployeeProfile, ProgressEntry, Kpi
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView
from .decorators import RoleRequiredMixin, role_required
from django.contrib.auth.models import User


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
