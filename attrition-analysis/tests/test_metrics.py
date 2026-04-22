import pandas as pd
from src.metrics import attrition_rate, attrition_by_department, satisfaction_summary


def test_attrition_rate_returns_expected_percent():
    df = pd.DataFrame(
        {
            "employee_id": [1, 2, 3, 4],
            "department": ["Sales", "Sales", "HR", "HR"],
            "attrition": ["Yes", "No", "No", "Yes"],
        }
    )
    assert attrition_rate(df) == 50.0


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


def test_satisfaction_summary_attrition_rate_is_within_group():
    # 2 employees at satisfaction 1, both left → 100%
    # 2 employees at satisfaction 4, none left  → 0%
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
