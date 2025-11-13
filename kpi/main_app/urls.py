from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path('kpis/', views.kpis_index , name='index'),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("dashboard/admin/", views.admin_dashboard, name="admin_dashboard"),
    path("dashboard/manager/", views.manager_dashboard, name="manager_dashboard"),
    path("dashboard/employee/", views.employee_dashboard, name="employee_dashboard"),
]
