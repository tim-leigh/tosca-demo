"""
Jira issue key : OCD-12
qTest test case: OCD-12 - Posted journal entry is visible in Manage Journals with the Posted status
qTest ID       : 107945095
"""
import os
import pytest
from tbox_sdk import Secret, V

BATCH_NAME = "GENERIC_BATCH_NAME_01"
ACCOUNTING_DATE = "2025-01-01"


def test_posted_journal_entry_visible_in_manage_journals_with_posted_status(tb) -> None:
    # Arrange – open application and sign in
    # Precondition: User is logged in with the General Accounting Manager role. Journal batch
    # GENERIC_BATCH_NAME_01 with accounting date 2025-01-01 has been successfully posted.
    tb.open(os.environ["ORACLE_URL"])
    page = tb.web
    page.textbox(id="userid").input(Secret.from_env("ORACLE_USER"))
    page.textbox(id="password").input(Secret.from_env("ORACLE_PASSWORD"))
    page.button(value="Sign In").click()

    # Step 1: Navigate to the Manage Journals screen from the General Accounting task panel.
    # TODO: confirm with tx scan
    page.element(inner_text="General Accounting", index=1).click()
    page.element(inner_text="Journals", index=1).click()
    page.element(inner_text="Manage Journals", index=1).click()
    # The Manage Journals search screen is displayed.
    page.element(css="h1,h2", index=1).verify(V.like("*Manage Journals*"))

    # Step 2: Search for the journal batch by entering batch name = GENERIC_BATCH_NAME_01 in the
    # search criteria and clicking Search.
    # TODO: confirm with tx scan
    page.textbox(id="BatchName").input(BATCH_NAME)
    page.button(value="Search").click()
    # Journal batch GENERIC_BATCH_NAME_01 is returned in the search results.
    page.element(css="table.results td", index=1).verify(V.like("*" + BATCH_NAME + "*"))

    # Step 3: Verify the status value displayed for journal batch GENERIC_BATCH_NAME_01 in the
    # Manage Journals results.
    # TODO: confirm with tx scan
    # The journal batch GENERIC_BATCH_NAME_01 displays a status of Posted (assumption: 'Posted' is
    # the exact status label; story author to confirm per quality finding F3), confirming it is
    # visible and correctly recorded in the ledger.
    page.element(css="td.journal-status", index=1).verify("Posted")
