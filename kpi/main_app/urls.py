from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("kpis/", views.kpis_index, name="index"),
    path("kpis/<int:kpi_id>/", views.kpis_detail, name="detail"),
    path("kpis/create/", views.KpiCreate.as_view(), name="kpis_create"),
    path("kpis/<int:pk>/update/", views.KpiUpdate.as_view(), name="kpis_update"),
    path("kpis/progress/", views.add_progress, name="progress"),
    path("kpis/employee/", views.employee_kpi, name="employee_kpi"),


]
