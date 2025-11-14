# main_app/forms.py
from django import forms
from .models import EmployeeKpi, EmployeeProfile, Kpi, ProgressEntry


class AssignKpiForm(forms.ModelForm):
    class Meta:
        model = EmployeeKpi
        fields = ["employee", "kpi", "target_value", "weight", "start_date", "end_date"]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }

    # when creating the forum run this func first
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        # check if the user assigining the employee is a manager
        if (
            user
            and hasattr(user, "employeeprofile")
            and user.employeeprofile.role == "manager"
        ):
            # check what department is the manager
            dept = user.employeeprofile.department
            # check all the employees that belong to the manager's dept
            self.fields["employee"].queryset = EmployeeProfile.objects.filter(
                department=dept, role="employee"
            )
            # check all the kpi's that relates to the manager dept
            self.fields["kpi"].queryset = Kpi.objects.filter(department=dept)
        # else:
        #     # default: show all employees who are role='employee' and all KPIs for the admin from his django admin portal
        #     self.fields["employee"].queryset = EmployeeProfile.objects.filter(
        #         role="employee"
        #     )
        #     self.fields["kpi"].queryset = Kpi.objects.all()


class KpiProgressForm(forms.ModelForm):
    employee_kpi = forms.ModelChoiceField(
        queryset=EmployeeKpi.objects.all(),
        label="Select KPI Assignment",
        widget=forms.Select(attrs={"class": "browser-default"}),
    )

    class Meta:
        model = ProgressEntry
        fields = ["employee_kpi", "value", "note", "date"]
        widgets = {
            "value": forms.NumberInput(attrs={"class": "validate"}),
            "note": forms.Textarea(attrs={"class": "materialize-textarea", "rows": 3}),
            "date": forms.DateInput(attrs={"type": "date", "class": ""}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user and hasattr(user, 'employeeprofile'):
            # filter to show only kpis assigned to this employee
            self.fields['employee_kpi'].queryset = EmployeeKpi.objects.filter(
                employee=user.employeeprofile
            ).select_related('kpi', 'employee__user')
