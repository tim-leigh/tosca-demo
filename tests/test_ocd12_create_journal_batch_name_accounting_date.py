"""
Jira issue: OCD-12
qTest test case: OCD-12 - User can create a new journal batch with a valid batch name and accounting date
qTest ID: 107947371
"""
import os
import pytest
import datetime
from tbox_sdk import Secret, V

BATCH_NAME = "GENERIC_BATCH_NAME_01"
ACCOUNTING_DATE = "2025-01-01"


def test_create_journal_batch_name_accounting_date(tb) -> None:
    # Precondition: User GENERIC_GA_USER_01 is logged in with the General Accounting Manager role.
    # The General Accounting Journal Entry screen is open.
    # A valid open accounting period exists in the target ledger.
    # Valid account segment combinations are available.

    # Arrange: open Oracle Cloud and sign in, then navigate to the Journal Entry screen
    tb.open(os.environ["ORACLE_URL"])
    page = tb.web
    page.textbox(id="username").input(Secret.from_env("ORACLE_USER"))
    page.textbox(id="password").input(Secret.from_env("ORACLE_PASSWORD"))
    page.button(value="Sign In").click()
    page.element(css="button.navigator-menu-icon").click()
    page.element(inner_text="General Accounting").click()
    page.element(inner_text="Journals").click()

    # Step 1: Click Create Journal Batch or the equivalent new-batch button on the General Accounting Journal Entry screen.
    page.button(value="Create Journal Batch").click()
    # A new journal batch form is displayed with empty fields for batch name, accounting date, and ledger.
    page.element(css="div.journal-batch-form").verify(V.like("*Journal Batch Name*"))

    # Step 2: Enter GENERIC_BATCH_NAME_01 in the Journal Batch Name field on the journal batch form.
    # TODO: confirm with tx scan
    page.element(css="input[label='Journal Batch Name']").input(BATCH_NAME)
    # GENERIC_BATCH_NAME_01 is accepted and displayed in the Journal Batch Name field without a validation error.
    page.element(css="input[label='Journal Batch Name']").verify(BATCH_NAME)

    # Step 3: Enter GENERIC_ACCOUNTING_DATE_01 = 2025-01-01 in the Accounting Date field on the journal batch form.
    # TODO: confirm with tx scan
    page.element(css="input[label='Accounting Date']").input(ACCOUNTING_DATE)
    # 2025-01-01 is accepted as the accounting date, falls within the open period, and is displayed without a validation error.
    page.element(css="input[label='Accounting Date']").verify(ACCOUNTING_DATE)

    # Step 4: Click Save or Continue on the journal batch form to persist the batch header.
    page.button(value="Save").click()
    # The journal batch GENERIC_BATCH_NAME_01 is saved with accounting date 2025-01-01 and the form advances
    # to the journal line entry section, confirming the batch was created successfully.
    page.element(css="div.journal-lines-section").verify(V.like("*" + BATCH_NAME + "*"))
