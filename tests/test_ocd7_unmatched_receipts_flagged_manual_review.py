"""
Jira issue: OCD-7
qTest test case: OCD-7 - Unmatched receipts in the lockbox file are flagged for manual review
qTest ID: 107947364
"""
import os
import pytest
from tbox_sdk import Secret, V

LOCKBOX_FILE = "GENERIC_LOCKBOX_FILE_01"
UNMATCHED_RECEIPT = "GENERIC_UNMATCHED_RECEIPT_01"


def test_unmatched_receipts_flagged_manual_review(tb) -> None:
    # Precondition: User GENERIC_AR_USER_01 is logged in with the Accounts Receivable Specialist role.
    # Lockbox file GENERIC_LOCKBOX_FILE_01 has been successfully imported (status 'Succeeded').
    # GENERIC_LOCKBOX_FILE_01 contains at least one receipt record GENERIC_UNMATCHED_RECEIPT_01
    # whose reference does not match any open invoice in Oracle Cloud AR for any customer.

    # Arrange: open Oracle Cloud and sign in
    tb.open(os.environ["ORACLE_URL"])
    page = tb.web
    page.textbox(id="username").input(Secret.from_env("ORACLE_USER"))
    page.textbox(id="password").input(Secret.from_env("ORACLE_PASSWORD"))
    page.button(value="Sign In").click()

    # Step 1: Navigate to Manage Receipts in Oracle Cloud Accounts Receivable.
    page.element(css="button.navigator-menu-icon").click()
    page.element(inner_text="Manage Receipts").click()
    # The Manage Receipts search screen is displayed.
    page.element(css="div.manage-receipts-screen").verify(V.like("*Manage Receipts*"))

    # Step 2: Enter the batch name or transmission reference from GENERIC_LOCKBOX_FILE_01 in the relevant filter field
    # on the Manage Receipts search screen and click Search.
    # TODO: confirm with tx scan
    page.element(css="input[label='Batch Name']").input(LOCKBOX_FILE)
    page.button(value="Search").click()
    # The search returns all receipts imported from GENERIC_LOCKBOX_FILE_01, including GENERIC_UNMATCHED_RECEIPT_01.
    page.element(css="table.search-results tbody tr").verify(V.like("*" + UNMATCHED_RECEIPT + "*"))

    # Step 3: Locate GENERIC_UNMATCHED_RECEIPT_01 in the search results and verify its status value.
    # GENERIC_UNMATCHED_RECEIPT_01 displays a status of 'Unapplied' (or the equivalent manual-review status),
    # indicating it has not been applied to any invoice and is flagged for manual review.
    # TODO: confirm with tx scan
    page.element(css="table.search-results td.receipt-status").verify("Unapplied")

    # Step 4: Click GENERIC_UNMATCHED_RECEIPT_01 to open its detail view and verify that no invoice application
    # records are present in the Applications section.
    page.element(css="table.search-results tbody tr a.receipt-link").click()
    # The Applications section is empty or contains no matched invoice entries, confirming the receipt remains
    # unmatched and is awaiting manual review rather than having been incorrectly applied.
    page.element(css="div.applications-section").verify(V.like("*No results*"))
