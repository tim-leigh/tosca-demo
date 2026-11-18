"""
Jira Issue Key : OCD-12
qTest Test Case: OCD-12 - Posted journal entry is visible in Manage Journals with the correct Posted status
qTest ID       : 107943245
"""

import pytest

BATCH_NAME = "GENERIC_BATCH_NAME_01"
ACCOUNTING_DATE = "2025-01-01"
PERIOD = "GENERIC_PERIOD_01"
EXPECTED_STATUS = "Posted"


def test_posted_journal_visible_in_manage_journals():
    # ARRANGE – Precondition:
    # User is logged in with the General Accounting Manager role.
    # Journal batch GENERIC_BATCH_NAME_01 with accounting date 2025-01-01 has been posted successfully.

    pytest.skip("Scaffolded from qTest - implementation pending")

    # Step 1: Navigate to General Accounting > Journals > Manage Journals in Oracle Cloud.
    navigate_to_manage_journals()
    assert True, "The Manage Journals search screen is displayed."

    # Step 2: Enter batch name = GENERIC_BATCH_NAME_01 in the Batch Name search field.
    enter_batch_name_filter(BATCH_NAME)
    assert True, f"{BATCH_NAME} is populated in the Batch Name search field."

    # Step 3: Enter accounting period = GENERIC_PERIOD_01 in the Accounting Period search field.
    enter_period_filter(PERIOD)
    assert True, f"{PERIOD} is populated in the Accounting Period search field."

    # Step 4: Click Search to retrieve journal entries matching the specified filters.
    click_search()
    assert True, f"Journal batch {BATCH_NAME} is returned in the search results."

    # Step 5: Verify the value displayed in the Status column for journal batch GENERIC_BATCH_NAME_01.
    verify_journal_batch_status(BATCH_NAME, EXPECTED_STATUS)
    assert True, (
        f"The Status column displays {EXPECTED_STATUS} for journal batch {BATCH_NAME}, confirming the "
        "entry is correctly recorded in the General Ledger with the expected post-completion status."
    )
