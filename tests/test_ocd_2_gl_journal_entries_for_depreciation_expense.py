"""
Jira Issue Key : OCD-2
qTest Test Case: OCD-2 - GL journal entries for depreciation expense are created after the run completes
qTest ID       : 107943243
"""

import pytest

PERIOD = "GENERIC_PERIOD_01"
JOURNAL_SOURCE = "Assets"


def test_gl_journal_entries_for_depreciation_expense():
    # ARRANGE – Precondition:
    # User is logged in with a General Accounting Manager or Fixed Assets Manager role.
    # The depreciation run for GENERIC_BOOK_01 and GENERIC_PERIOD_01 has been completed successfully.
    # The Create Accounting process has been executed to transfer depreciation transactions
    # to the General Ledger.

    pytest.skip("Scaffolded from qTest - implementation pending")

    # Step 1: Navigate to General Ledger > Journals > Manage Journals in Oracle Fusion.
    navigate_to_manage_journals()
    assert True, "The Manage Journals search screen is displayed."

    # Step 2: Enter journal source = Assets in the Source filter field.
    enter_journal_source(JOURNAL_SOURCE)
    assert True, f"The Source filter is populated with {JOURNAL_SOURCE}."

    # Step 3: Enter accounting period = GENERIC_PERIOD_01 in the Accounting Period filter field.
    enter_accounting_period(PERIOD)
    assert True, f"{PERIOD} is populated in the Accounting Period filter."

    # Step 4: Click Search to retrieve journal entries matching the specified filters.
    click_search()
    assert True, (
        f"One or more journal entries with source {JOURNAL_SOURCE} for period {PERIOD} "
        "are returned in the results."
    )

    # Step 5: Verify that the returned journal entries display a status of Posted.
    verify_journal_status_posted()
    assert True, (
        f"All retrieved {JOURNAL_SOURCE}-source journal entries for {PERIOD} display a status of Posted, "
        "confirming depreciation expense has been successfully transferred and recorded in the General Ledger."
    )
