from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse
from .models import EmployeeKpi, ProgressEntry, Kpi, EmployeeProfile, DEPARTMENT
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, View
from .forms import AssignKpiForm, KpiProgressForm
from django.contrib import messages
from .decorators import RoleRequiredMixin, role_required
from django.contrib.auth.models import User
from django.db.models import Q
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from datetime import datetime
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill

# Employee dashboard'
def dashboard(request):
    # return render(request, "dashboards/dashboard_home.html")
    profile = EmployeeProfile.objects.get(user=request.user)

    if profile.role == "admin":
        return admin_dashboard(request)
    elif profile.role == "manager":
        return manager_dashboard(request)
    else:
        return employee_dashboard(request)


def admin_dashboard(request):
    total_users = 8
    total_employees = 5

    context = {
        "total_users": total_users,
        "total_employees": total_employees,
    }
    return render(request, "dashboards/admin_dashboard.html", context)
    # total_users = User.objects.count()
    # total_employees = EmployeeProfile.objects.filter(role="employee").count()

    # context = {
    #     "total_users": total_users,
    #     "total_employees": total_employees,
    # }
    # kpis = EmployeeKpi.objects.all()
    # return render(request, "dashboards/admin_dashboard.html", {
    #     "profiles": profiles,
    #     "kpis": kpis,


def manager_dashboard(request):
    manager_name = "Shooq"
    department = "Information Technology"
    employees_count = 3

    context = {
        "manager_name": manager_name,
        "department": department,
        "employees_count": employees_count,
    }
    return render(request, "dashboards/manager_dashboard.html", context)
    # profile = EmployeeProfile.objects.get(user=request.user)
    # department = profile.department

    # employees_in_department = EmployeeProfile.objects.filter(department=department, role="employee").count()

    # context = {
    #     "manager": profile,
    #     "department": profile.get_department_display(),
    #     "employees_count": employees_in_department,
    # }

    # team = profile.team_members.all()
    # team_kpis = EmployeeKpi.objects.filter(employee__in=team)
    # return render(request, "dashboards/manager_dashboard.html", {
    #     "profile": profile,
    #     "team": team,
    #     "team_kpis": team_kpis,
    # })


def employee_dashboard(request):
    employee_name = "Maryam"
    department = "Sales & Marketing"
    role = "Employee"

    context = {
        "employee_name": employee_name,
        "department": department,
        "role": role,
    }
    return render(request, "dashboards/employee_dashboard.html", context)

    # profile = EmployeeProfile.objects.get(user=request.user)
    # return render(request, "dashboards/employee_dashboard.html", {"profile": profile})

    # profile = EmployeeProfile.objects.get(user=request.user)
    # kpis = profile.assigned_kpis.select_related("kpi").all()
    # return render(request, "dashboards/employee_dashboard.html", {
    #     "profile": profile,
    #     "kpis": kpis,
    # })


# Manager Dashboard

# Admin Dashboard


# create your views here
def home(request):
    return render(request, "home.html")


@login_required
@role_required(['admin'])
def kpis_index(request):
    kpis = Kpi.objects.all()
    return render(request, "kpi/index.html", {"kpis": kpis})



@login_required
def kpis_detail(request, kpi_id):
    kpi = Kpi.objects.get(id=kpi_id)
    return render(request, "kpi/detail.html", {"kpi": kpi})



class KpiCreate(RoleRequiredMixin, CreateView):
    model = Kpi
    fields = "__all__"
    success_url = "/kpis/"
    allowed_roles = ["admin"]



@login_required
@role_required(['employee'])
def add_progress(request):
    if request.method == 'POST':
        form = KpiProgressForm(request.POST, user=request.user)

        if form.is_valid():
            employee_kpi = form.cleaned_data['employee_kpi']

            if employee_kpi.status() == "Complete":
                messages.error(request, "This KPI is already complete. You cannot add more progress.")
                return redirect('employee_kpi')

            form.save()
            messages.success(request, "Progress added successfully!")

            return redirect('employee_kpi')

    else:
        form = KpiProgressForm(user=request.user)

    return render(request, 'kpi/progress.html', {'form': form})



@login_required
@role_required(['employee'])
def employee_kpi(request):
    employee_kpi = EmployeeKpi.objects.all()
    return render(request, "kpi/employee_kpi.html", {"employee_kpi": employee_kpi})


class KpiUpdate(RoleRequiredMixin, UpdateView):
    model = Kpi
    fields = "__all__"
    allowed_roles = ["admin"]


# unauthorized access page
def unauthorized(request):
    return render(request, "unauthorized.html")


@login_required
def profile(request):
    return render(request, "users/profile.html")

# Assign KPI: managers assign employees to KPI; KPIs & employees filtered by manager's department
@login_required
@role_required(['manager'])
def assign_kpi(request):
    # pass request.user into the form so it filters by department if user is manager
    form = AssignKpiForm(
        request.POST or None,
        user=(request.user if request.user.is_authenticated else None),
    )
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "KPI assigned successfully.")
            return redirect("employee_kpi_list")
    return render(request, "main_app/assign_kpi.html", {"form": form})

@login_required
@role_required(['manager'])
def employee_kpi_list(request):
    if (
        request.user.is_authenticated
        and hasattr(request.user, "employeeprofile")
        and request.user.employeeprofile.role == "manager"
    ):
        dept = request.user.employeeprofile.department
        # show only assignments where employee is in manager's department
        kpis = EmployeeKpi.objects.filter(employee__department=dept).select_related(
            "employee__user", "kpi"
        ).order_by('-id')
    else:
        kpis = EmployeeKpi.objects.select_related("employee__user", "kpi").all()

    # search functionality
    search_query = request.GET.get('search', '').strip()
    if search_query:
        kpis = kpis.filter(
            Q(employee__user__username__icontains=search_query) |
            Q(employee__user__first_name__icontains=search_query) |
            Q(employee__user__last_name__icontains=search_query) |
            Q(employee__job_role__icontains=search_query)
        )

    # filter by KPI
    kpi_filter = request.GET.get('kpi', '')
    if kpi_filter:
        kpis = kpis.filter(kpi__id=kpi_filter)

    # order by newest first
    kpis = kpis.order_by('-id')

    status_filter = request.GET.get('status', '')
    if status_filter:
        # convert the queryset to a list and filter by status since status is a method
        filtered_kpis = []
        for kpi in kpis:
            kpi_status = kpi.status().lower().replace(' ', '_')
            if kpi_status == status_filter:
                filtered_kpis.append(kpi)
        kpis = filtered_kpis
    else:
        # convert to list for consistency
        kpis = list(kpis)

    # get all KPIs for the filter dropdown
    if (
        request.user.is_authenticated
        and hasattr(request.user, "employeeprofile")
        and request.user.employeeprofile.role == "manager"
    ):
        dept = request.user.employeeprofile.department
        all_kpis = Kpi.objects.filter(department=dept)
    else:
        all_kpis = Kpi.objects.all()

    context = {
        'kpis': kpis,
        'all_kpis': all_kpis,
        'search_query': search_query,
        'kpi_filter': kpi_filter,
        'status_filter': status_filter,
    }
    return render(request, "main_app/employee_kpi_list.html", context)

@login_required
@role_required(['manager'])
def employee_kpi_edit(request, pk):
    kpi_assign = get_object_or_404(EmployeeKpi, pk=pk)
    if kpi_assign.progressentry_set.exists():
        messages.error(request, "Cannot edit KPI — progress already exists.")
        return redirect("employee_kpi_list")

    form = AssignKpiForm(
        request.POST or None,
        instance=kpi_assign,
        user=(request.user if request.user.is_authenticated else None),
    )
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "KPI updated successfully.")
        return redirect("employee_kpi_list")

    return render(
        request, "main_app/employee_kpi_edit.html", {"form": form, "kpi": kpi_assign}
    )

@login_required
@role_required(['manager'])
def employee_kpi_delete(request, pk):
    kpi_assign = get_object_or_404(EmployeeKpi, pk=pk)
    if kpi_assign.progressentry_set.exists():
        messages.error(request, "Cannot delete KPI — progress already exists.")
        return redirect("employee_kpi_list")

    if request.method == "POST":
        kpi_assign.delete()
        messages.success(request, "KPI assignment deleted.")
        return redirect("employee_kpi_list")

    return render(request, "main_app/employee_kpi_delete.html", {"kpi": kpi_assign})

@login_required
@role_required(['manager'])
def employee_kpi_detail(request, pk):
    kpi_assign = get_object_or_404(EmployeeKpi, pk=pk)
    progress_entries = kpi_assign.progressentry_set.order_by("date")
    return render(
        request,
        "main_app/employee_kpi_detail.html",
        {
            "kpi": kpi_assign,
            "progress_entries": progress_entries,
        },
    )

# reports views

# manager reports view with filtering
@login_required
@role_required(['manager'])
def manager_reports(request):
    dept = request.user.employeeprofile.department

    # get kpis that r filtered by manager's department
    kpis = EmployeeKpi.objects.filter(
        employee__department=dept
    ).select_related('employee__user', 'kpi').order_by('-id')

    # apply filters from get parameters
    search_query = request.GET.get('search', '').strip()
    if search_query:
        kpis = kpis.filter(
            Q(employee__user__username__icontains=search_query) |
            Q(employee__user__first_name__icontains=search_query) |
            Q(employee__user__last_name__icontains=search_query)
        )

    kpi_filter = request.GET.get('kpi', '')
    if kpi_filter:
        kpis = kpis.filter(kpi__id=kpi_filter)

    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')

    if start_date:
        kpis = kpis.filter(start_date__gte=start_date)
    if end_date:
        kpis = kpis.filter(end_date__lte=end_date)

    # get all kpis for the filter dropdown
    all_kpis = Kpi.objects.filter(department=dept)

    context = {
        'kpis': kpis,
        'all_kpis': all_kpis,
        'search_query': search_query,
        'kpi_filter': kpi_filter,
        'start_date': start_date,
        'end_date': end_date,
    }
    return render(request, "reports/manager_reports.html", context)

# admin reports view with filtering across all departments
@login_required
@role_required(['admin'])
def admin_reports(request):
    # get all kpis across all departments
    kpis = EmployeeKpi.objects.select_related('employee__user', 'kpi', 'employee', 'employee__manager','employee__manager__employeeprofile').order_by('-id')

    # apply filters from get parameters
    search_query = request.GET.get('search', '').strip()
    if search_query:
        kpis = kpis.filter(
            Q(employee__user__username__icontains=search_query) |
            Q(employee__user__first_name__icontains=search_query) |
            Q(employee__user__last_name__icontains=search_query) |
            Q(employee__manager__username__icontains=search_query) |
            Q(employee__manager__first_name__icontains=search_query) |
            Q(employee__manager__last_name__icontains=search_query)
        )

    # dept filterations
    department_filter = request.GET.get('department', '')
    if department_filter:
        kpis = kpis.filter(employee__department=department_filter)

    kpi_filter = request.GET.get('kpi', '')
    if kpi_filter:
        kpis = kpis.filter(kpi__id=kpi_filter)

    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')

    if start_date:
        kpis = kpis.filter(start_date__gte=start_date)
    if end_date:
        kpis = kpis.filter(end_date__lte=end_date)

    # get all kpis for the filter dropdown (all departments)
    all_kpis = Kpi.objects.all()

    # get all departments for filter
    all_departments = DEPARTMENT
    context = {
        'kpis': kpis,
        'all_kpis': all_kpis,
        'all_departments': all_departments,
        'search_query': search_query,
        'kpi_filter': kpi_filter,
        'department_filter': department_filter,
        'start_date': start_date,
        'end_date': end_date,
    }
    return render(request, "reports/admin_reports.html", context)

# exporting pdfs from manager side
@login_required
@role_required(['manager'])
def export_pdf(request):
    dept = request.user.employeeprofile.department

    # get filtered kpis same logic as manager_reports
    kpis = EmployeeKpi.objects.filter(
        employee__department=dept
    ).select_related('employee__user', 'kpi').order_by('-id')

    # apply filters
    search_query = request.GET.get('search', '').strip()
    if search_query:
        kpis = kpis.filter(
            Q(employee__user__username__icontains=search_query) |
            Q(employee__user__first_name__icontains=search_query) |
            Q(employee__user__last_name__icontains=search_query)
        )

    kpi_filter = request.GET.get('kpi', '')
    if kpi_filter:
        kpis = kpis.filter(kpi__id=kpi_filter)

    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')

    if start_date:
        kpis = kpis.filter(start_date__gte=start_date)
    if end_date:
        kpis = kpis.filter(end_date__lte=end_date)

    # create PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=KPI_Report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'

    # create PDF document
    doc = SimpleDocTemplate(response, pagesize=landscape(A4))
    elements = []

    # Styles
    styles = getSampleStyleSheet()

    # Title
    title = Paragraph(
        f"<b>KPI Performance Report</b><br/>{datetime.now().strftime('%B %d, %Y')}",
        styles['Title']
    )
    elements.append(title)
    elements.append(Spacer(1, 0.3*inch))

    # table data
    data = [['KPI', 'Employee', 'Target', 'Current', 'Progress', 'Status', 'Period']]

    for kpi in kpis:
        data.append([
            kpi.kpi.title,
            kpi.employee.user.first_name + " " + kpi.employee.user.last_name,
            str(kpi.target_value),
            str(kpi.total_progress()),
            f"{kpi.progress_percentage()}%",
            kpi.status(),
            f"{kpi.start_date}\n - {kpi.end_date}"
        ])

    # Create table
    table = Table(data, repeatRows=1)
    table.setStyle(TableStyle([
        # Header styling
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0F172A')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),

        # Body styling
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),

        # Alternating rows
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
    ]))

    elements.append(table)

    # Build PDF
    doc.build(elements)

    return response

# exporting excel from manager side
@login_required
@role_required(['manager'])
def export_excel(request):
    dept = request.user.employeeprofile.department

    # get filtered kpis same logic as manager_reports
    kpis = EmployeeKpi.objects.filter(
        employee__department=dept
    ).select_related('employee__user', 'kpi').order_by('-id')

    # apply filters from get parameter
    search_query = request.GET.get('search', '').strip()
    if search_query:
        kpis = kpis.filter(
            Q(employee__user__username__icontains=search_query) |
            Q(employee__user__first_name__icontains=search_query) |
            Q(employee__user__last_name__icontains=search_query)
        )

    kpi_filter = request.GET.get('kpi', '')
    if kpi_filter:
        kpis = kpis.filter(kpi__id=kpi_filter)

    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')

    if start_date:
        kpis = kpis.filter(start_date__gte=start_date)
    if end_date:
        kpis = kpis.filter(end_date__lte=end_date)

    # createing workbook
    wb = Workbook()

    # select the active sheet
    sheet = wb.active
    sheet.title = "KPI Report"

    # header styling
    header_fill = PatternFill(start_color="0F172A", end_color="0F172A", fill_type="solid")
    header_font = Font(color="FFFFFF", bold=True, size=12)

    # title
    sheet.merge_cells('A1:G1')
    title_cell = sheet['A1']
    title_cell.value = f"KPI Performance Report - {datetime.now().strftime('%Y-%m-%d')}"
    title_cell.font = Font(bold=True, size=14)
    title_cell.alignment = Alignment(horizontal='center')

    # headers
    headers = ['KPI', 'Employee', 'Target', 'Current Value', 'Progress %', 'Status', 'Period']
    for col_num, header in enumerate(headers, 1):
        cell = sheet.cell(row=3, column=col_num)
        cell.value = header
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal='center')

    # data
    for row_num, kpi in enumerate(kpis, 4):
        sheet.cell(row=row_num, column=1).value = kpi.kpi.title
        sheet.cell(row=row_num, column=2).value = kpi.employee.user.first_name + " " + kpi.employee.user.last_name
        sheet.cell(row=row_num, column=3).value = kpi.target_value
        sheet.cell(row=row_num, column=4).value = kpi.total_progress()
        sheet.cell(row=row_num, column=5).value = f"{kpi.progress_percentage()}%"
        sheet.cell(row=row_num, column=6).value = kpi.status()
        sheet.cell(row=row_num, column=7).value = f"{kpi.start_date} → {kpi.end_date}"

    # auto-adjust column widths
    for column_cells in sheet.columns:
        max_length = 0
        column_letter = None

        for cell in column_cells:
            # skip merged cells
            if hasattr(cell, 'column_letter'):
                if column_letter is None:
                    column_letter = cell.column_letter
                try:
                    if cell.value:
                        cell_length = len(str(cell.value))
                        if cell_length > max_length:
                            max_length = cell_length
                except:
                    pass

        if column_letter and max_length > 0:
            adjusted_width = min(max_length + 2, 50)  # here capping at 50 to avoid overly wide columns
            sheet.column_dimensions[column_letter].width = adjusted_width

    # prepare response
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename=KPI_Report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'

    wb.save(response)
    return response


# Admin export to PDF
@login_required
@role_required(['admin'])
def admin_export_pdf(request):
    # get filtered kpis - same logic as admin_reports
    kpis = EmployeeKpi.objects.select_related(
        'employee__user',
        'kpi',
        'employee__manager'
    ).order_by('-id')

    # apply filters
    search_query = request.GET.get('search', '').strip()
    if search_query:
        kpis = kpis.filter(
            Q(employee__user__username__icontains=search_query) |
            Q(employee__user__first_name__icontains=search_query) |
            Q(employee__user__last_name__icontains=search_query) |
            Q(employee__manager__username__icontains=search_query) |
            Q(employee__manager__first_name__icontains=search_query) |
            Q(employee__manager__last_name__icontains=search_query)
        )

    department_filter = request.GET.get('department', '')
    if department_filter:
        kpis = kpis.filter(employee__department=department_filter)

    kpi_filter = request.GET.get('kpi', '')
    if kpi_filter:
        kpis = kpis.filter(kpi__id=kpi_filter)

    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')

    if start_date:
        kpis = kpis.filter(start_date__gte=start_date)
    if end_date:
        kpis = kpis.filter(end_date__lte=end_date)

    # create PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=Admin_KPI_Report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'

    # create PDF document
    doc = SimpleDocTemplate(response, pagesize=landscape(A4))
    elements = []

    # Styles
    styles = getSampleStyleSheet()

    # Title
    title = Paragraph(
        f"<b>Admin KPI Performance Report</b><br/>{datetime.now().strftime('%B %d, %Y')}",
        styles['Title']
    )
    elements.append(title)
    elements.append(Spacer(1, 0.3*inch))

    # table data
    data = [['KPI', 'Employee', 'Manager', 'Dept', 'Target', 'Current', 'Progress', 'Status', 'Period']]

    for kpi in kpis:
        manager_name = f"{kpi.employee.manager.first_name} {kpi.employee.manager.last_name}" if kpi.employee.manager else 'N/A'
        employee_name = f"{kpi.employee.user.first_name} {kpi.employee.user.last_name}"
        data.append([
            kpi.kpi.title[:20],
            employee_name,
            manager_name,
            kpi.employee.get_department_display()[:35],
            str(kpi.target_value),
            str(kpi.total_progress()),
            f"{kpi.progress_percentage()}%",
            kpi.status(),
            f"{kpi.start_date}\n{kpi.end_date}"
        ])

    # Create table
    table = Table(data, repeatRows=1)
    table.setStyle(TableStyle([
        # Header styling
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0F172A')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),

        # Body styling
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 7),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),

        # Alternating rows
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
    ]))

    elements.append(table)

    # Build PDF
    doc.build(elements)

    return response


# Admin export to Excel
@login_required
@role_required(['admin'])
def admin_export_excel(request):
    # get filtered kpis - same logic as admin_reports
    kpis = EmployeeKpi.objects.select_related(
        'employee__user',
        'kpi',
        'employee__manager'
    ).order_by('-id')

    # apply filters from get parameter
    search_query = request.GET.get('search', '').strip()
    if search_query:
        kpis = kpis.filter(
            Q(employee__user__username__icontains=search_query) |
            Q(employee__user__first_name__icontains=search_query) |
            Q(employee__user__last_name__icontains=search_query) |
            Q(employee__manager__username__icontains=search_query) |
            Q(employee__manager__first_name__icontains=search_query) |
            Q(employee__manager__last_name__icontains=search_query)
        )

    department_filter = request.GET.get('department', '')
    if department_filter:
        kpis = kpis.filter(employee__department=department_filter)

    kpi_filter = request.GET.get('kpi', '')
    if kpi_filter:
        kpis = kpis.filter(kpi__id=kpi_filter)

    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')

    if start_date:
        kpis = kpis.filter(start_date__gte=start_date)
    if end_date:
        kpis = kpis.filter(end_date__lte=end_date)

    # creating workbook
    wb = Workbook()

    # select the active sheet
    sheet = wb.active
    sheet.title = "Admin KPI Report"

    # header styling
    header_fill = PatternFill(start_color="0F172A", end_color="0F172A", fill_type="solid")
    header_font = Font(color="FFFFFF", bold=True, size=12)

    # title
    sheet.merge_cells('A1:J1')
    title_cell = sheet['A1']
    title_cell.value = f"Admin KPI Performance Report - {datetime.now().strftime('%Y-%m-%d')}"
    title_cell.font = Font(bold=True, size=14)
    title_cell.alignment = Alignment(horizontal='center')

    # headers
    headers = ['KPI', 'Employee', 'Manager', 'Department', 'Target', 'Current Value', 'Progress %', 'Weight %', 'Status', 'Period']
    for col_num, header in enumerate(headers, 1):
        cell = sheet.cell(row=3, column=col_num)
        cell.value = header
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal='center')

    # data
    for row_num, kpi in enumerate(kpis, 4):
        manager_name = f"{kpi.employee.manager.first_name} {kpi.employee.manager.last_name}" if kpi.employee.manager else 'No Manager'
        employee_name = f"{kpi.employee.user.first_name} {kpi.employee.user.last_name}"

        sheet.cell(row=row_num, column=1).value = kpi.kpi.title
        sheet.cell(row=row_num, column=2).value = employee_name
        sheet.cell(row=row_num, column=3).value = manager_name
        sheet.cell(row=row_num, column=4).value = kpi.employee.get_department_display()
        sheet.cell(row=row_num, column=5).value = kpi.target_value
        sheet.cell(row=row_num, column=6).value = kpi.total_progress()
        sheet.cell(row=row_num, column=7).value = f"{kpi.progress_percentage()}%"
        sheet.cell(row=row_num, column=8).value = f"{kpi.weight}%"
        sheet.cell(row=row_num, column=9).value = kpi.status()
        sheet.cell(row=row_num, column=10).value = f"{kpi.start_date} → {kpi.end_date}"

    # auto-adjust column widths
    for column_cells in sheet.columns:
        max_length = 0
        column_letter = None

        for cell in column_cells:
            if hasattr(cell, 'column_letter'):
                if column_letter is None:
                    column_letter = cell.column_letter
                try:
                    if cell.value:
                        cell_length = len(str(cell.value))
                        if cell_length > max_length:
                            max_length = cell_length
                except:
                    pass

        if column_letter and max_length > 0:
            adjusted_width = min(max_length + 2, 50)
            sheet.column_dimensions[column_letter].width = adjusted_width

    # prepare response
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename=Admin_KPI_Report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'

    wb.save(response)
    return response
