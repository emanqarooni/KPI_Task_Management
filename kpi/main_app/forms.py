from django import forms
from .models import EmployeeKpi, EmployeeProfile, Kpi

class AssignKpiForm(forms.ModelForm):
    class Meta:
        model = EmployeeKpi
        fields = ['employee', 'kpi', 'target_value', 'weight', 'start_date', 'end_date']

    employee = forms.ModelChoiceField(
        queryset=EmployeeProfile.objects.filter(role="employee"),
        label="Choose Employee"
    )

    kpi = forms.ModelChoiceField(
        queryset=Kpi.objects.all(),
        label="Choose KPI"
    )

    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
