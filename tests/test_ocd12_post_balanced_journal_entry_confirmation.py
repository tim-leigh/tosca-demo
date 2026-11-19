"""
Jira issue: OCD-12
qTest test case: OCD-12 - User can successfully post a balanced journal entry and receive a posting confirmation
qTest ID: 107947368
"""
import os
import pytest
from tbox_sdk import Secret, V

BATCH_NAME = "GENERIC_BATCH_NAME_01"
SEGMENT_DEBIT = "GENERIC_SEGMENT_DEBIT_01"
SEGMENT_CREDIT = "GENERIC_SEGMENT_CREDIT_01"
LINE_AMOUNT = "1000"
ACCOUNTING_DATE = "2025-01-01"


def test_post_balanced_journal_entry_confirmation(tb) -> None:
    # Precondition: User GENERIC_GA_USER_01 is logged in with the General Accounting Manager role.
    # Journal batch GENERIC_BATCH_NAME_01 has been created and contains balanced journal lines with
    # GENERIC_SEGMENT_DEBIT_01 debited 1000 and GENERIC_SEGMENT_CREDIT_01 credited 1000.
    # The accounting period for date 2025-01-01 is open.

    # Arrange: open Oracle Cloud, sign in, navigate to the journal batch
    tb.open(os.environ["ORACLE_URL"])
    page = tb.web
    page.textbox(id="username").input(Secret.from_env("ORACLE_USER"))
    page.textbox(id="password").input(Secret.from_env("ORACLE_PASSWORD"))
    page.button(value="Sign In").click()
    page.element(css="button.navigator-menu-icon").click()
    page.element(inner_text="General Accounting").click()
    page.element(inner_text="Journals").click()
    # TODO: confirm with tx scan
    page.element(css="input[label='Journal Batch Name']").input(BATCH_NAME)
    page.button(value="Search").click()
    page.element(css="table.search-results tbody tr a.batch-link").click()

    # Step 1: Verify the Post button or action is enabled on the journal batch GENERIC_BATCH_NAME_01 screen.
    # The Post button is enabled, indicating the system recognises the journal lines as balanced and permits posting.
    page.button(value="Post").verify(V.like("*Post*"))

    # Step 2: Click the Post button on the journal batch GENERIC_BATCH_NAME_01 screen.
    page.button(value="Post").click()
    # The system initiates the posting process for GENERIC_BATCH_NAME_01.
    page.element(css="div.posting-in-progress").verify(V.like("*posting*"))

    # Step 3: Verify that a posting confirmation message or status indicator is displayed on screen after the Post action completes.
    # A confirmation message (e.g., 'Journal posted successfully' or equivalent) is displayed,
    # or the journal header status updates to 'Posted', confirming the posting action completed successfully.
    page.element(css="div.journal-status, div.confirmation-message").verify(V.like("*Posted*"))
