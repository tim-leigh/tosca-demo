"""
Jira issue key : OCD-12
qTest test case: OCD-12 - User can create a new journal batch with a valid batch name and accounting date
qTest ID       : 107945093
"""
import os
import pytest
from tbox_sdk import Secret, V

BATCH_NAME = "GENERIC_BATCH_NAME_01"
ACCOUNTING_DATE = "2025-01-01"


def test_create_journal_batch_with_valid_batch_name_and_accounting_date(tb) -> None:
    # Arrange – open application and sign in
    # Precondition: User is logged in with the General Accounting Manager role. The Journal
    # Entry screen is open. A valid open accounting period exists in the target ledger for
    # date 2025-01-01.
    tb.open(os.environ["ORACLE_URL"])
    page = tb.web
    page.textbox(id="userid").input(Secret.from_env("ORACLE_USER"))
    page.textbox(id="password").input(Secret.from_env("ORACLE_PASSWORD"))
    page.button(value="Sign In").click()

    # Navigate to Create Journal screen (precondition fulfilment)
    # TODO: confirm with tx scan
    page.element(inner_text="General Accounting", index=1).click()
    page.element(inner_text="Journals", index=1).click()
    page.element(inner_text="Create Journal", index=1).click()

    # Step 1: Enter the journal batch name = GENERIC_BATCH_NAME_01 in the Batch Name field.
    # TODO: confirm with tx scan
    page.textbox(id="BatchName").input(BATCH_NAME)
    # The batch name GENERIC_BATCH_NAME_01 is accepted and displayed in the Batch Name field without validation errors.
    page.textbox(id="BatchName").verify(BATCH_NAME)

    # Step 2: Enter the accounting date = 2025-01-01 in the Accounting Date field.
    # TODO: confirm with tx scan
    page.textbox(id="AccountingDate").input(ACCOUNTING_DATE)
    # The accounting date 2025-01-01 is accepted, falls within the open period, and no period-closed error is displayed.
    page.textbox(id="AccountingDate").verify(ACCOUNTING_DATE)

    # Step 3: Save the journal batch header by clicking Save or the equivalent action.
    page.button(value="Save").click()
    # The journal batch header is saved successfully and the screen proceeds to allow journal line entry.
    page.element(css="div.confirmation,div.journal-lines-section", index=1).verify(V.like("*saved*"))
