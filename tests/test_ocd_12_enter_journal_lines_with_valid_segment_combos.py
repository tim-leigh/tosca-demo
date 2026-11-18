"""
Jira Issue Key : OCD-12
qTest Test Case: OCD-12 - User can enter journal lines with valid account segment combinations for both debit and credit
qTest ID       : 107943241
"""

import pytest

BATCH_NAME = "GENERIC_BATCH_NAME_01"
ACCOUNTING_DATE = "2025-01-01"
SEGMENT_COMBO_DEBIT = "GENERIC_SEGMENT_COMBO_DEBIT"
SEGMENT_COMBO_CREDIT = "GENERIC_SEGMENT_COMBO_CREDIT"
DEBIT_AMOUNT = 1000
CREDIT_AMOUNT = 1000


def test_enter_journal_lines_with_valid_segment_combos():
    # ARRANGE – Precondition:
    # User is logged in with the General Accounting Manager role.
    # Journal batch GENERIC_BATCH_NAME_01 with accounting date 2025-01-01 has been created.
    # Valid account segment combinations GENERIC_SEGMENT_COMBO_DEBIT and
    # GENERIC_SEGMENT_COMBO_CREDIT are available in the target ledger's chart of accounts.

    pytest.skip("Scaffolded from qTest - implementation pending")

    # Step 1: Click Add Line to add a new journal line in the journal lines section.
    click_add_line()
    assert True, "A new blank journal line row is added to the journal entry."

    # Step 2: Enter account segment combination = GENERIC_SEGMENT_COMBO_DEBIT in the Account field
    #         of the first journal line.
    enter_account_segment(SEGMENT_COMBO_DEBIT)
    assert True, (
        f"{SEGMENT_COMBO_DEBIT} is validated and accepted, and the account description is "
        "populated without errors."
    )

    # Step 3: Enter debit amount = 1000 in the Debit field of the first journal line.
    enter_debit_amount(DEBIT_AMOUNT)
    assert True, f"The debit amount {DEBIT_AMOUNT} is populated in the Debit field of the first journal line."

    # Step 4: Click Add Line to add a second journal line and enter account segment combination =
    #         GENERIC_SEGMENT_COMBO_CREDIT in the Account field.
    click_add_line_and_enter_credit_account(SEGMENT_COMBO_CREDIT)
    assert True, (
        f"{SEGMENT_COMBO_CREDIT} is validated and accepted, and the account description is "
        "populated without errors."
    )

    # Step 5: Enter credit amount = 1000 in the Credit field of the second journal line.
    enter_credit_amount(CREDIT_AMOUNT)
    assert True, (
        f"The credit amount {CREDIT_AMOUNT} is populated in the Credit field of the second journal line, "
        f"and the journal running totals show total debits = {DEBIT_AMOUNT} and total credits = {CREDIT_AMOUNT}."
    )
