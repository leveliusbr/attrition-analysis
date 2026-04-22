import pandas as pd
from src.metrics import (
    attrition_rate,
    attrition_by_department,
    attrition_by_overtime,
    average_income_by_attrition,
    satisfaction_summary,
)


# ---------------------------------------------------------------------------
# attrition_rate
# ---------------------------------------------------------------------------

def test_attrition_rate_returns_expected_percent():
    df = pd.DataFrame(
        {
            "employee_id": [1, 2, 3, 4],
            "attrition": ["Yes", "No", "No", "Yes"],
        }
    )
    assert attrition_rate(df) == 50.0


def test_attrition_rate_zero_percent():
    df = pd.DataFrame({"employee_id": [1, 2], "attrition": ["No", "No"]})
    assert attrition_rate(df) == 0.0


def test_attrition_rate_hundred_percent():
    df = pd.DataFrame({"employee_id": [1, 2], "attrition": ["Yes", "Yes"]})
    assert attrition_rate(df) == 100.0


# ---------------------------------------------------------------------------
# attrition_by_department
# ---------------------------------------------------------------------------

def test_attrition_by_department_returns_expected_columns():
    df = pd.DataFrame(
        {
            "employee_id": [1, 2, 3, 4],
            "department": ["Sales", "Sales", "HR", "HR"],
            "attrition": ["Yes", "No", "No", "Yes"],
        }
    )
    result = attrition_by_department(df)
    assert list(result.columns) == ["department", "employees", "leavers", "attrition_rate"]


def test_attrition_by_department_computes_correct_values():
    df = pd.DataFrame(
        {
            "employee_id": [1, 2, 3, 4, 5],
            "department": ["Sales", "Sales", "HR", "HR", "HR"],
            "attrition": ["Yes", "No", "Yes", "Yes", "No"],
        }
    )
    result = attrition_by_department(df)
    hr = result[result["department"] == "HR"].iloc[0]
    sales = result[result["department"] == "Sales"].iloc[0]
    assert hr["employees"] == 3
    assert hr["leavers"] == 2
    assert hr["attrition_rate"] == 66.67
    assert sales["employees"] == 2
    assert sales["leavers"] == 1
    assert sales["attrition_rate"] == 50.0


def test_attrition_by_department_sorted_descending_by_rate():
    df = pd.DataFrame(
        {
            "employee_id": [1, 2, 3, 4, 5],
            "department": ["Sales", "Sales", "HR", "HR", "HR"],
            "attrition": ["Yes", "No", "Yes", "Yes", "No"],
        }
    )
    result = attrition_by_department(df)
    rates = result["attrition_rate"].tolist()
    assert rates == sorted(rates, reverse=True)


# ---------------------------------------------------------------------------
# attrition_by_overtime
# ---------------------------------------------------------------------------

def test_attrition_by_overtime_returns_expected_columns():
    df = pd.DataFrame(
        {
            "employee_id": [1, 2],
            "overtime": ["Yes", "No"],
            "attrition": ["Yes", "No"],
        }
    )
    result = attrition_by_overtime(df)
    assert list(result.columns) == ["overtime", "employees", "leavers", "attrition_rate"]


def test_attrition_by_overtime_computes_correct_values():
    df = pd.DataFrame(
        {
            "employee_id": [1, 2, 3, 4],
            "overtime": ["Yes", "Yes", "No", "No"],
            "attrition": ["Yes", "Yes", "Yes", "No"],
        }
    )
    result = attrition_by_overtime(df)
    yes_row = result[result["overtime"] == "Yes"].iloc[0]
    no_row = result[result["overtime"] == "No"].iloc[0]
    assert yes_row["employees"] == 2
    assert yes_row["leavers"] == 2
    assert yes_row["attrition_rate"] == 100.0
    assert no_row["employees"] == 2
    assert no_row["leavers"] == 1
    assert no_row["attrition_rate"] == 50.0


# ---------------------------------------------------------------------------
# average_income_by_attrition
# ---------------------------------------------------------------------------

def test_average_income_by_attrition_returns_expected_columns():
    df = pd.DataFrame(
        {"attrition": ["Yes", "No"], "monthly_income": [4000, 6000]}
    )
    result = average_income_by_attrition(df)
    assert list(result.columns) == ["attrition", "avg_monthly_income"]


def test_average_income_by_attrition_computes_correct_means():
    df = pd.DataFrame(
        {
            "attrition": ["Yes", "Yes", "No", "No"],
            "monthly_income": [3000, 5000, 7000, 9000],
        }
    )
    result = average_income_by_attrition(df)
    yes_income = result[result["attrition"] == "Yes"]["avg_monthly_income"].iloc[0]
    no_income = result[result["attrition"] == "No"]["avg_monthly_income"].iloc[0]
    assert yes_income == 4000.0
    assert no_income == 8000.0


# ---------------------------------------------------------------------------
# satisfaction_summary
# ---------------------------------------------------------------------------

def test_satisfaction_summary_attrition_rate_is_within_group():
    # satisfaction 1: 2 employees, both left  → 100%
    # satisfaction 4: 2 employees, none left  → 0%
    df = pd.DataFrame(
        {
            "employee_id": [1, 2, 3, 4],
            "job_satisfaction": [1, 1, 4, 4],
            "attrition": ["Yes", "Yes", "No", "No"],
        }
    )
    result = satisfaction_summary(df)
    sat1 = result[result["job_satisfaction"] == 1]["attrition_rate"].iloc[0]
    sat4 = result[result["job_satisfaction"] == 4]["attrition_rate"].iloc[0]
    assert sat1 == 100.0
    assert sat4 == 0.0


def test_satisfaction_summary_partial_attrition():
    # satisfaction 2: 4 employees, 1 left → 25%
    df = pd.DataFrame(
        {
            "employee_id": [1, 2, 3, 4],
            "job_satisfaction": [2, 2, 2, 2],
            "attrition": ["Yes", "No", "No", "No"],
        }
    )
    result = satisfaction_summary(df)
    rate = result[result["job_satisfaction"] == 2]["attrition_rate"].iloc[0]
    assert rate == 25.0


def test_satisfaction_summary_sorted_ascending_by_satisfaction():
    df = pd.DataFrame(
        {
            "employee_id": [1, 2, 3, 4],
            "job_satisfaction": [3, 1, 4, 2],
            "attrition": ["Yes", "No", "No", "Yes"],
        }
    )
    result = satisfaction_summary(df)
    levels = result["job_satisfaction"].tolist()
    assert levels == sorted(levels)
