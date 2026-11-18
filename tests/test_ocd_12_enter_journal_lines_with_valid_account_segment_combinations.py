"""
Jira issue key : OCD-12
qTest test case: OCD-12 - User can enter journal lines with valid account segment combinations covering both debit and credit
qTest ID       : 107945094
"""
import os
import pytest
from tbox_sdk import Secret, V

BATCH_NAME = "GENERIC_BATCH_NAME_01"
ACCOUNTING_DATE = "2025-01-01"
SEGMENT_DEBIT = "GENERIC_SEGMENT_DEBIT_01"
SEGMENT_CREDIT = "GENERIC_SEGMENT_CREDIT_01"
DEBIT_AMOUNT = "1000"
CREDIT_AMOUNT = "1000"


def test_enter_journal_lines_with_valid_account_segment_combinations(tb) -> None:
    # Arrange – open application and sign in
    # Precondition: User is logged in with the General Accounting Manager role. Journal batch
    # GENERIC_BATCH_NAME_01 with accounting date 2025-01-01 has been created. Valid account
    # segment combinations GENERIC_SEGMENT_DEBIT_01 and GENERIC_SEGMENT_CREDIT_01 are
    # available in the target ledger.
    tb.open(os.environ["ORACLE_URL"])
    page = tb.web
    page.textbox(id="userid").input(Secret.from_env("ORACLE_USER"))
    page.textbox(id="password").input(Secret.from_env("ORACLE_PASSWORD"))
    page.button(value="Sign In").click()

    # Navigate to journal batch (precondition fulfilment)
    # TODO: confirm with tx scan
    page.element(inner_text="General Accounting", index=1).click()
    page.element(inner_text="Journals", index=1).click()
    page.element(inner_text="Manage Journals", index=1).click()
    page.textbox(id="BatchName").input(BATCH_NAME)
    page.button(value="Search").click()
    page.element(inner_text=BATCH_NAME, index=1).click()

    # Step 1: Click Add Line or equivalent to create the first journal line on the journal entry form.
    # TODO: confirm with tx scan
    page.button(value="Add Line").click()
    # A new journal line row is added and ready for input.
    page.element(css="tr.journal-line-new,tr.line-row", index=1).verify(V.like("*"))

    # Step 2: Enter account segment combination = GENERIC_SEGMENT_DEBIT_01 and debit amount = 1000
    # in the first journal line fields.
    # TODO: confirm with tx scan
    page.textbox(id="AccountSegment1").input(SEGMENT_DEBIT)
    page.textbox(id="DebitAmount1").input(DEBIT_AMOUNT)
    # The debit line is accepted with account GENERIC_SEGMENT_DEBIT_01 and a debit amount of 1000;
    # no segment validation error is displayed.
    page.textbox(id="DebitAmount1").verify(DEBIT_AMOUNT)

    # Step 3: Click Add Line to create the second journal line and enter account segment combination =
    # GENERIC_SEGMENT_CREDIT_01 and credit amount = 1000.
    # TODO: confirm with tx scan
    page.button(value="Add Line").click()
    page.textbox(id="AccountSegment2").input(SEGMENT_CREDIT)
    page.textbox(id="CreditAmount2").input(CREDIT_AMOUNT)
    # The credit line is accepted with account GENERIC_SEGMENT_CREDIT_01 and a credit amount of 1000;
    # no segment validation error is displayed.
    page.textbox(id="CreditAmount2").verify(CREDIT_AMOUNT)

    # Step 4: Verify the journal balance indicator on the journal entry screen.
    # TODO: confirm with tx scan
    # Total debits equal total credits (both 1000), and the journal is indicated as balanced,
    # enabling the Post action.
    page.element(css="div.balance-indicator,span.journal-balance", index=1).verify(V.like("*balanced*"))
