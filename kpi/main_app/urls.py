from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path('kpis/', views.kpis_index , name='index'),
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
]
