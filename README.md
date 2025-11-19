# KPI_Task_Management
## Date: 11/11/2025
### By: Eman Qarooni, Eman Rauf, Shooq BinZaiman, Fatima Zaid

[Eman Qarooni Github](https://github.com/emanqarooni) | [Eman Rauf Github](https://github.com/emannn077) |
[Shooq BinZaiman Github](https://github.com/shooqbinzaiman) |
[Fatima Zaid](https://github.com/fatima-zaid)

## 🧭 Overview

The KPI Task Management System is a web-based platform built using Django that helps organizations monitor employee performance efficiently through Key Performance Indicators (KPIs).

The system provides role-based access for Admins, Managers, and Employees, allowing each role to interact with KPIs differently:

- Admins can manage users, departments, and KPIs.

- Managers can assign KPIs and monitor the performance of their department members.

- Employees can view their assigned KPIs and update their progress regularly.

The goal of this system is to streamline performance tracking, improve accountability, and enhance transparency within the workplace.

## 🎯 Main Objective

To build a simple, efficient, and scalable system that helps organizations:

- Define and assign KPIs for each employee.

- Track performance progress over time.

- Simplify communication between managers and their teams.

- Generate a clear overview of departmental and individual achievements.

## 🧩 Functional Requirements

### *Admin :*

- Manage user accounts and roles (Admin, Manager, Employee).

- Create, edit, and delete KPI categories.

- Assign KPIs to departments or managers.

- View all employees and KPI statistics.

### *Manager :*

- View all employees within their department.

- Assign KPIs to employees.

- Track progress entries submitted by employees.

- Monitor department performance in real time.

### *Employee :*

- View their own KPIs.

- Submit progress updates (daily or weekly).

- Add notes or comments related to their KPI performance.

- See overall progress percentage and days remaining for each KPI.

## 🧠 Features (Planned and Completed)

- *Role-based dashboards :* Admin, Manager, and Employee each have separate views.

- *KPI management :* Create, assign, and monitor Key Performance Indicators.

- *Progress tracking :* Employees can log progress entries tied to assigned KPIs.

- *Performance overview :* Managers and Admins can view completion percentages and remaining time.

- *Department-based filtering :* Managers only see KPIs and employees under their department.

- *Dynamic dashboards :* Display data visually and update automatically when KPIs are changed.

- *Authentication system :* Users log in and are redirected to their respective dashboard.

- *Clean and simple UI :* Beginner-friendly HTML/CSS structure following CH4 standards.

- *Future expansion :* Integrate AI suggestions for performance improvements.


## ⚙️ Tools & Technologies

- Framework: *Django (Python)*
- Frontend: *HTML, CSS, Daisy UI*
- Backend: *Django Models, Views, and Templates*
- Database: *Postgre SQL*
- Version Control: *Git & GitHub*
- Project Management: *Trello and Teams*
- Utilities: *Pillow (for images), Django Auth System*

A Trello board was used to track development progress and can be viewed [here](https://trello.com/b/gjUDr0Cr/project-4-kpi).
### ***Screenshots***
### Wireframe:
![Wireframe4](Wireframe4.png)
### ERD:
![ERD](ERD4.png)

### ***Credits***

#### 1. CSS:
[Daisyui](https://daisyui.com/docs/install/django/)

#### 2. PDF exporting using reportlab:
[Reportlab](https://docs.reportlab.com/pdf-accessibility/)
/ [Medium](https://medium.com/@saijalshakya/generating-pdf-with-reportlab-in-django-ee0235c2f133)

#### 3. Excel exporting using openpyxl:
[Geeksforgeeks](https://www.geeksforgeeks.org/python/introduction-to-python-openpyxl/)
/ [Stackoverflow](https://stackoverflow.com/questions/33217306/return-openpyxl-workbook-object-as-httpresponse-in-django-is-it-possible)

#### 4. Notifications:
[Stackoverflow](https://stackoverflow.com/questions/72264677/how-can-i-implement-notifications-system-in-django)
/ [Readthedocs](https://django-notification-system.readthedocs.io/en/latest/)
/ [Medium](https://medium.com/@anas-issath/i-built-a-real-time-notification-system-in-django-3bb5cb97916d)

### 5. Chartjs:
[Chartjs](https://pypi.org/project/django-chartjs/)

### 6. Forget Password:
[forget password](https://www.pythontutorial.net/django-tutorial/django-password-reset/)

### 7. Custome Decorator for roles based access
[Custom Decorator](https://medium.com/@amar.raw011/implementing-custom-decorators-for-role-based-login-in-django-what-i-learned-0806b66bd8ae)
