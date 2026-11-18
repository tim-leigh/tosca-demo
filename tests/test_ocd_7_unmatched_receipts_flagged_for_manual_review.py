"""
Jira issue key : OCD-7
qTest test case: OCD-7 - Unmatched receipts in the lockbox file are flagged for manual review
qTest ID       : 107945088
"""
import os
import pytest
from tbox_sdk import Secret, V

UNMATCHED_RECEIPT = "GENERIC_UNMATCHED_RECEIPT_01"
LOCKBOX_FILE = "GENERIC_LOCKBOX_FILE_01"


def test_unmatched_receipts_flagged_for_manual_review(tb) -> None:
    # Arrange – open application and sign in
    # Precondition: User is logged in with the Accounts Receivable Manager role (assumption).
    # AutoLockbox import of GENERIC_LOCKBOX_FILE_01 has completed successfully. The lockbox
    # file contains at least one receipt record GENERIC_UNMATCHED_RECEIPT_01 whose reference
    # does not correspond to any open invoice in the system.
    tb.open(os.environ["ORACLE_URL"])
    page = tb.web
    page.textbox(id="userid").input(Secret.from_env("ORACLE_USER"))
    page.textbox(id="password").input(Secret.from_env("ORACLE_PASSWORD"))
    page.button(value="Sign In").click()

    # Step 1: Navigate to the Manage Receipts screen via Receivables > Receipts > Manage Receipts.
    # TODO: confirm with tx scan
    page.element(inner_text="Receivables", index=1).click()
    page.element(inner_text="Receipts", index=1).click()
    page.element(inner_text="Manage Receipts", index=1).click()
    # The Manage Receipts screen is displayed.
    page.element(css="h1,h2", index=1).verify(V.like("*Manage Receipts*"))

    # Step 2: Search for receipt = GENERIC_UNMATCHED_RECEIPT_01 by its reference number or amount.
    # TODO: confirm with tx scan
    page.textbox(id="ReceiptRef").input(UNMATCHED_RECEIPT)
    page.button(value="Search").click()
    # Receipt GENERIC_UNMATCHED_RECEIPT_01 is listed in the search results.
    page.element(css="table.results td", index=1).verify(V.like("*" + UNMATCHED_RECEIPT + "*"))

    # Step 3: Verify the status of receipt GENERIC_UNMATCHED_RECEIPT_01 on the Manage Receipts screen.
    # TODO: confirm with tx scan
    # Receipt GENERIC_UNMATCHED_RECEIPT_01 displays a status of Unapplied (or equivalent
    # flagged-for-review status — story author to confirm exact label per quality finding F3),
    # indicating it has been held for manual review.
    page.element(css="td.receipt-status", index=1).verify("Unapplied")
