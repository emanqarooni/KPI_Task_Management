from django.urls import path, include
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("kpis/", views.kpis_index, name="index"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("dashboard/admin/", views.admin_dashboard, name="admin_dashboard"),
    path("dashboard/manager/", views.manager_dashboard, name="manager_dashboard"),
    path("dashboard/employee/", views.employee_dashboard, name="employee_dashboard"),
    path("kpis/<int:kpi_id>/", views.kpis_detail, name="detail"),
    path("kpis/create/", views.KpiCreate.as_view(), name="kpis_create"),
    path("kpis/<int:pk>/update/", views.KpiUpdate.as_view(), name="kpis_update"),
    path("unauthorized/", views.unauthorized, name="unauthorized"),
    path("profile/", views.profile, name="profile"),
    path("kpis/progress/", views.add_progress, name="progress"),
    path("kpis/employee/", views.employee_kpi, name="employee_kpi"),
    # kpi assignments urls from manager portal
    path('assign-kpi/', views.assign_kpi, name='assign_kpi'),
    path('employee-kpis/', views.employee_kpi_list, name='employee_kpi_list'),
    path('employee-kpi/<int:pk>/edit/', views.employee_kpi_edit, name='employee_kpi_edit'),
    path('employee-kpi/<int:pk>/delete/', views.employee_kpi_delete, name='employee_kpi_delete'),
    path('employee-kpi/<int:pk>/', views.employee_kpi_detail, name='employee_kpi_detail'),

    # reports urls for admin and manager portal
    path('reports/', views.manager_reports, name='reports'),
    path('reports/export-pdf/', views.export_pdf, name='export_pdf'),
    path('reports/export-excel/', views.export_excel, name='export_excel'),
    path('admin-reports/', views.admin_reports, name='admin_reports'),
    path('reports/admin_export-pdf/', views.admin_export_pdf, name='admin_export_pdf'),
    path('reports/admin_export-excel/', views.admin_export_excel, name='admin_export_excel'),

    # for admin only
    path("activity-logs/", views.activity_logs, name="activity_logs"),

    # notifications for manager and employee only
    path('notifications/', views.notifications, name='notifications'),

    # for ai feature
    path("ai/kpi-insights/", views.ai_kpi_insights, name="ai_kpi_insights"),
    path("admin-dashboard/ai-insights/", views.ai_admin_insights, name="ai_admin_insights"),
    path("employee/ai-coach/", views.ai_employee_coach, name="ai_employee_coach"),

]
