# main_app/forms.py
from django import forms
from .models import EmployeeKpi, EmployeeProfile, Kpi, ProgressEntry
from datetime import date


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
        else:
            # default: show all employees who are role='employee' and all KPIs for the admin from his django admin portal
            self.fields["employee"].queryset = EmployeeProfile.objects.filter(
                role="employee"
            )
            self.fields["kpi"].queryset = Kpi.objects.all()

    def clean_start_date(self):
        # validate that start date is not in the past
        start_date = self.cleaned_data.get('start_date')

        if start_date and start_date < date.today():
            raise forms.ValidationError(
                "Start date cannot be in the past. Please select today or a future date."
            )

        return start_date

    def clean_end_date(self):
        # validate that end_date is not in the past
        end_date = self.cleaned_data.get('end_date')

        if end_date and end_date < date.today():
            raise forms.ValidationError(
                "End date cannot be in the past. Please select today or a future date."
            )

        return end_date

    def clean_target_value(self):
        # validating that the target_value is a positive number
        target_value = self.cleaned_data.get('target_value')

        if target_value is not None and target_value <= 0:
            raise forms.ValidationError(
                "Target value must be greater than 0."
            )

        return target_value

    def clean_weight(self):
        # validate that weight is between 0 and 100 cannot be more thn that
        weight = self.cleaned_data.get('weight')

        if weight is not None:
            if weight <= 0:
                raise forms.ValidationError(
                    "Weight must be greater than 0."
                )
            if weight > 100:
                raise forms.ValidationError(
                    "Weight cannot exceed 100%."
                )

        return weight

    # clean method is used for validating multiple fields at once, and i am using this to check for if the scenario1: if the employee has already a kpi that may overlap the dates, scenario2: if the employee is assigned to the kpi but when the manager assign a new kpi there may be a partial overlap in dates, and the third thing is making sure that if there is no overlapping for the newly assigned kpi to the employee then the forum will be submitted
    def clean(self):
            # cross-field validation
            cleaned_data = super().clean()
            start_date = cleaned_data.get('start_date')
            end_date = cleaned_data.get('end_date')
            employee = cleaned_data.get('employee')
            kpi = cleaned_data.get('kpi')

            # validate that end_date is after start_date
            if start_date and end_date:
                if end_date < start_date:
                    raise forms.ValidationError(
                        "End date must be after or equal to the start date."
                    )

            # check for duplicate KPI assignments (same employee + same kpi + overlapping dates)
            if employee and kpi and start_date and end_date:
                # exclude the current instance if we're editing
                existing_kpis = EmployeeKpi.objects.filter(
                    employee=employee,
                    kpi=kpi
                )

                if self.instance.pk:
                    existing_kpis = existing_kpis.exclude(pk=self.instance.pk)

                # check for overlapping date ranges
                for existing_kpi in existing_kpis:
                    # check if dates overlap
                    if not (end_date < existing_kpi.start_date or start_date > existing_kpi.end_date):
                        raise forms.ValidationError(
                            f"This employee already has the KPI '{kpi.title}' assigned for an overlapping period "
                            f"({existing_kpi.start_date} to {existing_kpi.end_date}). "
                            f"Please choose different dates or a different KPI."
                        )

            return cleaned_data


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
