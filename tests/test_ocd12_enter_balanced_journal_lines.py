"""
Jira issue: OCD-12
qTest test case: OCD-12 - User can enter balanced journal lines with valid debit and credit account segment combinations
qTest ID: 107947370
"""
import os
import pytest
from tbox_sdk import Secret, V

BATCH_NAME = "GENERIC_BATCH_NAME_01"
ACCOUNTING_DATE = "2025-01-01"
SEGMENT_DEBIT = "GENERIC_SEGMENT_DEBIT_01"
SEGMENT_CREDIT = "GENERIC_SEGMENT_CREDIT_01"
LINE_AMOUNT = "1000"


def test_enter_balanced_journal_lines(tb) -> None:
    # Precondition: User GENERIC_GA_USER_01 is logged in with the General Accounting Manager role.
    # Journal batch GENERIC_BATCH_NAME_01 has been created with accounting date 2025-01-01.
    # The journal line entry section is displayed.
    # Valid account segment combinations GENERIC_SEGMENT_DEBIT_01 and GENERIC_SEGMENT_CREDIT_01 are available.

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

    # Step 1: Click Add Line or the equivalent button in the journal lines section to create the first journal line.
    page.button(value="Add Line").click()
    # A new blank journal line row is added to the lines grid.
    page.element(css="table.journal-lines tbody tr:last-child").verify(V.like("*Account*"))

    # Step 2: Enter GENERIC_SEGMENT_DEBIT_01 in the Account field of the first journal line.
    # TODO: confirm with tx scan
    page.element(css="table.journal-lines tbody tr:last-child input[label='Account']").input(SEGMENT_DEBIT)
    # GENERIC_SEGMENT_DEBIT_01 is accepted as a valid account segment combination and populated without a validation error.
    page.element(css="table.journal-lines tbody tr:last-child input[label='Account']").verify(SEGMENT_DEBIT)

    # Step 3: Enter GENERIC_LINE_AMOUNT_01 = 1000 in the Debit field of the first journal line.
    # TODO: confirm with tx scan
    page.element(css="table.journal-lines tbody tr:last-child input[label='Debit']").input(LINE_AMOUNT)
    # 1000 is populated in the Debit field and the Credit field for the same line remains zero.
    page.element(css="table.journal-lines tbody tr:last-child input[label='Debit']").verify(LINE_AMOUNT)

    # Step 4: Click Add Line to create a second journal line, then enter GENERIC_SEGMENT_CREDIT_01 in the Account field.
    page.button(value="Add Line").click()
    # TODO: confirm with tx scan
    page.element(css="table.journal-lines tbody tr:last-child input[label='Account']").input(SEGMENT_CREDIT)
    # GENERIC_SEGMENT_CREDIT_01 is accepted as a valid account segment combination and populated without a validation error.
    page.element(css="table.journal-lines tbody tr:last-child input[label='Account']").verify(SEGMENT_CREDIT)

    # Step 5: Enter GENERIC_LINE_AMOUNT_01 = 1000 in the Credit field of the second journal line.
    # TODO: confirm with tx scan
    page.element(css="table.journal-lines tbody tr:last-child input[label='Credit']").input(LINE_AMOUNT)
    # 1000 is populated in the Credit field of the second line, and the running balance indicator shows
    # total debits equal total credits (both 1000), satisfying the balance requirement and enabling the Post action.
    page.element(css="table.journal-lines tbody tr:last-child input[label='Credit']").verify(LINE_AMOUNT)
