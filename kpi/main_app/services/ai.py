import google.generativeai as genai
from django.conf import settings
from dotenv import load_dotenv
import os

load_dotenv()
genai.configure(api_key=settings.GOOGLE_API_KEY)


def generate_kpi_insights(text_data, mode="manager"):
    try:
        model = genai.GenerativeModel("models/gemini-2.5-flash")

#ai feature prompt for employee
        if mode == "employee":
            prompt = f"""
You are a friendly, supportive **Personal KPI Coach**.

You need to guide the employee based on:
- Their KPIs
- Progress percentages
- Deadlines
- Notes
- Workload
- Status of each KPI

Tone:
- Warm
- Motivational
- Clear
- No blaming

Provide SECTIONS:

**1. Warm Greeting**
Address the employee directly by name if possible.

**2. Summary of Their Active KPIs**
- Progress
- Deadlines
- Notes
- What each KPI means for their role

**3. What They Are Doing Well**
Highlight strengths, improvements, consistency.

**4. What Needs Improvement (Gently)**
- Avoid negativity
- Give helpful suggestions
- Focus only on active KPIs

**5. Today's Top 3 Focus Tasks**
Give clear, short action items.

**6. Deadline Reminders**
Mention only upcoming or urgent deadlines.

**7. Motivation Message**
Encouraging closing message.

Employee KPI Data:
{text_data}
"""

## ai feature prompt for
        elif mode == "manager":
            prompt = f"""
You are an expert KPI performance analyst helping a MANAGER understand their team's performance.

IMPORTANT RULES:
- Today's date is 2025-11-17. Ignore “future” dates.
- Only analyze the “Current Task (Detailed)” section deeply.
- Anything under “Previous Tasks” must be treated as completed or inactive.
- Do NOT criticize completed/old tasks.
- Focus ONLY on active KPIs.
- Be constructive and positive.

Provide:
1. Employees performing well (CURRENT tasks)
2. Employees who are behind (CURRENT tasks)
3. KPIs at risk or delayed
4. Short team performance summary
5. Positive, helpful recommendations for the manager

KPI Data:
{text_data}
"""

##ai feature for admin only
        else:
            prompt = f"""
You are an expert ORGANIZATIONAL KPI ANALYST.

Goal:
Provide a company-wide overview across:
- Departments
- Managers
- Employees

IMPORTANT RULES:
- Today is 2025-11-17. Ignore “future” dates.
- Employees with “No active KPI” represent operational gaps (NOT failures).
- Completed KPIs should NOT be criticized.
- Focus on trends, workload distribution, and departmental performance.

SECTIONS TO PROVIDE:

**1. Department Overviews**
- Active KPIs
- Completed KPIs
- Progress averages
- Risks or bottlenecks
- Which departments are ahead/behind

**2. Manager Performance**
- Team performance levels
- Productivity patterns
- Workload balance
- Support needed by managers

**3. Employee Snapshot**
- ONLY current KPIs
- Identify high performers
- Identify those behind
- Flag employees with no KPI (need assignment)

**4. Organization-Wide Risks**
- Missing KPIs
- Overdue tasks
- Training gaps
- HR or workflow issues

**5. Positive, Actionable Recommendations**
- Operational improvements
- KPI assignment suggestions
- Training/support priorities for admin

KPI Data:
{text_data}
"""

        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return f"AI error: {str(e)}"
