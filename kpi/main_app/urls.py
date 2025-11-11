from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path('kpis/', views.kpis_index , name='index'),
    path('kpis/<int:kpi_id>/', views.kpis_detail , name='detail'),

]
