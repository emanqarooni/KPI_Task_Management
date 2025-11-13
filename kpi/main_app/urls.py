from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("kpis/", views.kpis_index, name="index"),
    path("kpis/<int:kpi_id>/", views.kpis_detail, name="detail"),
    path("kpis/create/", views.KpiCreate.as_view(), name="kpis_create"),
    path("kpis/<int:pk>/update/", views.KpiUpdate.as_view(), name="kpis_update"),
    path("kpis/progress/", views.add_progress, name="progress"),

    # kpi assignments urls from manager portal
    path('assign-kpi/', views.assign_kpi, name='assign_kpi'),
    path('employee-kpis/', views.employee_kpi_list, name='employee_kpi_list'),
    path('employee-kpi/<int:pk>/edit/', views.employee_kpi_edit, name='employee_kpi_edit'),
    path('employee-kpi/<int:pk>/delete/', views.employee_kpi_delete, name='employee_kpi_delete'),
    path('employee-kpi/<int:pk>/', views.employee_kpi_detail, name='employee_kpi_detail'),
]
