# main_app/forms.py
from django import forms
from .models import EmployeeKpi, EmployeeProfile, Kpi

class AssignKpiForm(forms.ModelForm):
    class Meta:
        model = EmployeeKpi
        fields = ['employee', 'kpi', 'target_value', 'weight', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user and hasattr(user, "employeeprofile") and user.employeeprofile.role == "manager":
            dept = user.employeeprofile.department
            self.fields['employee'].queryset = EmployeeProfile.objects.filter(department=dept, role='employee')
            self.fields['kpi'].queryset = Kpi.objects.filter(department=dept)
        else:
            # default: show all employees who are role='employee' and all KPIs
            self.fields['employee'].queryset = EmployeeProfile.objects.filter(role='employee')
            self.fields['kpi'].queryset = Kpi.objects.all()
