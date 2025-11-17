import google.generativeai as genai
from django.conf import settings
from dotenv import load_dotenv
import os


load_dotenv()

genai.configure(api_key=settings.GOOGLE_API_KEY)


def generate_kpi_insights(text_data, mode="manager"):
    try:
        model = genai.GenerativeModel("models/gemini-2.5-flash")

        # prompt for manager
        if mode == "manager":
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
            5. Positive, helpful recommendations for the manager to guide the team

            KPI Data:
            {text_data}
            """

        # Prompt for admin

        else:
            prompt = f"""
            You are an expert ORGANIZATIONAL KPI ANALYST.

            Your goal is to give a company-wide overview across:
            - Departments
            - Managers
            - Employees

            IMPORTANT RULES:
            - Today is 2025-11-17. Do NOT treat dates as future.
            - When an employee has “No active KPI”, treat that as an operational gap (not a failure).
            - Completed KPIs should NOT be criticized.
            - Focus on departmental performance, workload distribution, manager effectiveness.

            Provide CLEAR SECTIONS:

            **1. Department Overviews**
            - Active KPIs
            - Overall progress level
            - Risks or imbalances
            - Which departments are ahead/behind

            **2. Manager Performance**
            - How each manager’s team is performing
            - Who needs more support
            - Any patterns (high workload, low engagement)

            **3. Employee Snapshot**
            - Highlight only CURRENT KPIs
            - Identify employees performing well
            - Identify employees falling behind
            - List employees with no current KPIs (these need new assignments)

            **4. Organization-Wide Risks**
            - Missing KPIs
            - Blockers
            - Skill/resource gaps

            **5. Positive, Actionable Recommendations for ADMIN**
            - What departments need attention
            - Where to add KPIs
            - Where to train or support employees
            - Any operational improvements

            KPI Data:
            {text_data}
            """

        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return f"AI error: {str(e)}"
