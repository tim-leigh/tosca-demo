"""
Jira Issue Key : OCD-12
qTest Test Case: OCD-12 - User can create a new journal batch with a valid batch name and accounting date
qTest ID       : 107943234
"""

import pytest

BATCH_NAME = "GENERIC_BATCH_NAME_01"
ACCOUNTING_DATE = "2025-01-01"
PERIOD = "GENERIC_PERIOD_01"


def test_create_journal_batch_with_valid_name_and_date():
    # ARRANGE – Precondition:
    # User is logged in with the General Accounting Manager role.
    # The Create Journal Batch screen is open.
    # Accounting period GENERIC_PERIOD_01, which contains the date 2025-01-01, is open
    # in the target ledger.

    pytest.skip("Scaffolded from qTest - implementation pending")

    # Step 1: Enter batch name = GENERIC_BATCH_NAME_01 in the Batch Name field.
    enter_batch_name(BATCH_NAME)
    assert True, f"{BATCH_NAME} is accepted and displayed in the Batch Name field without validation errors."

    # Step 2: Enter accounting date = 2025-01-01 in the Accounting Date field.
    enter_accounting_date(ACCOUNTING_DATE)
    assert True, (
        f"{ACCOUNTING_DATE} is accepted in the Accounting Date field and the system resolves it "
        f"to open period {PERIOD} without errors."
    )

    # Step 3: Verify that no mandatory-field or validation errors are displayed on the journal batch header.
    verify_no_validation_errors()
    assert True, (
        f"The batch header shows {BATCH_NAME} and accounting date {ACCOUNTING_DATE} with no field "
        "validation errors, confirming the batch is ready for journal line entry."
    )
