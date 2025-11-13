from django import forms
from .models import EmployeeKpi, ProgressEntry


class KpiProgressForm(forms.ModelForm):
    employee_kpi = forms.ModelChoiceField(
        queryset=EmployeeKpi.objects.all(),
        label="Select KPI Assignment",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    class Meta:
        model = ProgressEntry
        fields = ["employee_kpi", "value", "note", "date"]
        widgets = {
            "value": forms.NumberInput(attrs={"class": "form-control"}),
            "note": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        }
