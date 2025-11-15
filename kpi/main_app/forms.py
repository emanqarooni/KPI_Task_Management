# main_app/forms.py
from django import forms
from .models import EmployeeKpi, EmployeeProfile, Kpi, ProgressEntry


class AssignKpiForm(forms.ModelForm):
    class Meta:
        model = EmployeeKpi
        fields = ["employee", "kpi", "target_value", "weight", "start_date", "end_date"]
        widgets = {
            "start_date": forms.DateInput(attrs={
                "type": "date",
                "class": "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            }),
            "end_date": forms.DateInput(attrs={
                "type": "date",
                "class": "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            }),
            "employee": forms.Select(attrs={
                "class": "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            }),
            "kpi": forms.Select(attrs={
                "class": "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            }),
            "target_value": forms.NumberInput(attrs={
                "class": "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            }),
            "weight": forms.NumberInput(attrs={
                "class": "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            }),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if (
            user
            and hasattr(user, "employeeprofile")
            and user.employeeprofile.role == "manager"
        ):
            dept = user.employeeprofile.department
            self.fields["employee"].queryset = EmployeeProfile.objects.filter(
                department=dept, role="employee"
            )
            self.fields["kpi"].queryset = Kpi.objects.filter(department=dept)
        else:
            self.fields["employee"].queryset = EmployeeProfile.objects.filter(
                role="employee"
            )
            self.fields["kpi"].queryset = Kpi.objects.all()


class KpiProgressForm(forms.ModelForm):
    employee_kpi = forms.ModelChoiceField(
        queryset=EmployeeKpi.objects.all(),
        label="Select KPI Assignment",
        widget=forms.Select(attrs={
            "class": "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 py-2 px-3"
        }),
    )

    class Meta:
        model = ProgressEntry
        fields = ["employee_kpi", "value", "note", "date"]
        widgets = {
            "value": forms.NumberInput(attrs={
                "class": "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500",
                "step": "0.01"
            }),
            "note": forms.Textarea(attrs={
                "class": "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500",
                "rows": 3
            }),
            "date": forms.DateInput(attrs={
                "type": "date",
                "class": "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            }),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user and hasattr(user, 'employeeprofile'):
            self.fields['employee_kpi'].queryset = EmployeeKpi.objects.filter(
                employee=user.employeeprofile
            ).select_related('kpi', 'employee__user')
