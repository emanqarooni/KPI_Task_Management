from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import EmployeeKpi, ProgressEntry, Kpi
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, View
from .forms import KpiProgressForm


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


