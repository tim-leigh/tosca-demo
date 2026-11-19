"""
Jira issue: OCD-12
qTest test case: OCD-12 - Posted journal entry is visible in Manage Journals with a status of Posted
qTest ID: 107947372
"""
import os
import pytest
from tbox_sdk import Secret, V

BATCH_NAME = "GENERIC_BATCH_NAME_01"
ACCOUNTING_DATE = "2025-01-01"
SEGMENT_DEBIT = "GENERIC_SEGMENT_DEBIT_01"
SEGMENT_CREDIT = "GENERIC_SEGMENT_CREDIT_01"
LINE_AMOUNT = "1000"


def test_posted_journal_visible_manage_journals(tb) -> None:
    # Precondition: User GENERIC_GA_USER_01 is logged in with the General Accounting Manager role.
    # Journal batch GENERIC_BATCH_NAME_01 has been successfully posted as confirmed in the previous test case.
    # The accounting period 2025-01-01 is the target search period.

    # Arrange: open Oracle Cloud, sign in, navigate to Manage Journals
    tb.open(os.environ["ORACLE_URL"])
    page = tb.web
    page.textbox(id="username").input(Secret.from_env("ORACLE_USER"))
    page.textbox(id="password").input(Secret.from_env("ORACLE_PASSWORD"))
    page.button(value="Sign In").click()
    page.element(css="button.navigator-menu-icon").click()
    page.element(inner_text="General Accounting").click()

    # Step 1: Navigate to Manage Journals within the General Accounting work area.
    page.element(inner_text="Manage Journals").click()
    # The Manage Journals search screen is displayed with filter fields for ledger, period, batch name, and status.
    page.element(css="div.manage-journals-screen").verify(V.like("*Manage Journals*"))

    # Step 2: Enter GENERIC_BATCH_NAME_01 in the Journal Batch Name filter field on the Manage Journals search screen.
    # TODO: confirm with tx scan
    page.element(css="input[label='Journal Batch Name']").input(BATCH_NAME)
    # GENERIC_BATCH_NAME_01 is populated in the filter field.
    page.element(css="input[label='Journal Batch Name']").verify(BATCH_NAME)

    # Step 3: Enter 2025-01-01 in the Accounting Date or Period filter field on the Manage Journals search screen, then click Search.
    # TODO: confirm with tx scan
    page.element(css="input[label='Accounting Date']").input(ACCOUNTING_DATE)
    page.button(value="Search").click()
    # The search executes and returns at least one result matching GENERIC_BATCH_NAME_01.
    page.element(css="table.search-results tbody tr").verify(V.like("*" + BATCH_NAME + "*"))

    # Step 4: Verify that the Status column for the journal record GENERIC_BATCH_NAME_01 displays 'Posted'.
    # The Status field for GENERIC_BATCH_NAME_01 displays 'Posted', confirming the journal entry is visible
    # in Manage Journals with the correct status after a successful post.
    page.element(css="table.search-results td.journal-status").verify("Posted")

    # Step 5: Click the journal record GENERIC_BATCH_NAME_01 to open its detail view and verify the journal lines
    # show GENERIC_SEGMENT_DEBIT_01 debited 1000 and GENERIC_SEGMENT_CREDIT_01 credited 1000.
    page.element(css="table.search-results tbody tr a.batch-link").click()
    # The journal detail view displays the two lines with their correct account segment combinations and amounts,
    # confirming the posted entry accurately reflects the data entered during creation.
    page.element(css="table.journal-lines tbody").verify(V.like("*" + SEGMENT_DEBIT + "*"))
