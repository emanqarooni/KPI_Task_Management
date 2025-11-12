from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse
from .models import EmployeeKpi, ProgressEntry, Kpi
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView
from .decorators import RoleRequiredMixin
# create your views here
def home(request):
    return render(request, "home.html")


def kpis_index(request):
    kpis = Kpi.objects.all()
    return render(request, "kpi/index.html", {"kpis": kpis})


def kpis_detail(request, kpi_id):
    kpi = Kpi.objects.get(id=kpi_id)
    return render(request, "kpi/detail.html", {"kpi": kpi})

class KpiCreate(CreateView):
    model = Kpi
    fields = "__all__"
    success_url="/kpis/"
    allowed_role=['admin']
    
class KpiUpdate(UpdateView):
    model = Kpi
    fields = "__all__"
    allowed_role=['admin']


# unauthorized access page
def unauthorized(request):
    return render(request,"unauthorized.html")

