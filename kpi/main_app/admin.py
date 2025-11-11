from django.contrib import admin
from .models import Kpi, EmployeeKpi, ProgressEntry

# Register your models here.
admin.site.register(Kpi)
admin.site.register(EmployeeKpi)
admin.site.register(ProgressEntry)
