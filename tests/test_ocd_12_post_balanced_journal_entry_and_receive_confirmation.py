"""
Jira issue key : OCD-12
qTest test case: OCD-12 - User can successfully post the balanced journal entry and receive a confirmation
qTest ID       : 107945092
"""
import os
import pytest
from tbox_sdk import Secret, V

BATCH_NAME = "GENERIC_BATCH_NAME_01"
ACCOUNTING_DATE = "2025-01-01"
SEGMENT_DEBIT = "GENERIC_SEGMENT_DEBIT_01"
SEGMENT_CREDIT = "GENERIC_SEGMENT_CREDIT_01"


def test_post_balanced_journal_entry_and_receive_confirmation(tb) -> None:
    # Arrange – open application and sign in
    # Precondition: User is logged in with the General Accounting Manager role. Journal batch
    # GENERIC_BATCH_NAME_01 has been created with accounting date 2025-01-01, debit line
    # GENERIC_SEGMENT_DEBIT_01 for 1000, and credit line GENERIC_SEGMENT_CREDIT_01 for 1000.
    # The journal is balanced (total debits = total credits = 1000).
    tb.open(os.environ["ORACLE_URL"])
    page = tb.web
    page.textbox(id="userid").input(Secret.from_env("ORACLE_USER"))
    page.textbox(id="password").input(Secret.from_env("ORACLE_PASSWORD"))
    page.button(value="Sign In").click()

    # Navigate to the journal batch (precondition fulfilment)
    # TODO: confirm with tx scan
    page.element(inner_text="General Accounting", index=1).click()
    page.element(inner_text="Journals", index=1).click()
    page.element(inner_text="Manage Journals", index=1).click()
    page.textbox(id="BatchName").input(BATCH_NAME)
    page.button(value="Search").click()
    page.element(inner_text=BATCH_NAME, index=1).click()

    # Step 1: Click the Post button on the journal entry screen for batch GENERIC_BATCH_NAME_01.
    page.button(value="Post").click()
    # The Post action is accepted by the system and processing begins.
    page.element(css="div.posting-status,div.process-indicator", index=1).verify(V.like("*posting*"))

    # Step 2: Wait for the posting process to complete and observe the screen for a confirmation indicator.
    # TODO: confirm with tx scan
    # A confirmation is displayed — either an on-screen confirmation message, a toast notification,
    # or the journal status visibly changes — indicating that the journal entry has been posted
    # successfully (assumption: at least one form of confirmation is shown; story author to confirm
    # exact mechanism per quality finding F2).
    page.element(css="div.confirmation,div.toast,td.journal-status", index=1).verify(V.like("*Posted*"))
