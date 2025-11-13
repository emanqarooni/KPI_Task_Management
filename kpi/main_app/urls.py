from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path('kpis/', views.kpis_index , name='index'),

    # kpi assignments urls from manager portal
    path('assign-kpi/', views.assign_kpi, name='assign_kpi'),
    path('employee-kpis/', views.employee_kpi_list, name='employee_kpi_list'),
]
