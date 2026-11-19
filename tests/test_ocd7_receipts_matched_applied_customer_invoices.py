"""
Jira issue: OCD-7
qTest test case: OCD-7 - Receipts from an imported lockbox file are matched and applied to correct open customer invoices
qTest ID: 107947361
"""
import os
import pytest
from tbox_sdk import Secret, V

CUSTOMER = "GENERIC_CUSTOMER_01"
INVOICE_REF = "GENERIC_INVOICE_REF_01"


def test_receipts_matched_applied_customer_invoices(tb) -> None:
    # Precondition: User GENERIC_AR_USER_01 is logged in with the Accounts Receivable Specialist role.
    # Lockbox file GENERIC_LOCKBOX_FILE_01 has been successfully imported (status 'Succeeded').
    # GENERIC_LOCKBOX_FILE_01 contains a receipt for customer GENERIC_CUSTOMER_01 with a reference
    # matching open invoice GENERIC_INVOICE_REF_01. Invoice GENERIC_INVOICE_REF_01 is open and
    # outstanding in Oracle Cloud AR.

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

    # Step 2: Enter GENERIC_CUSTOMER_01 in the Customer filter field on the Manage Receipts search screen and click Search.
    # TODO: confirm with tx scan
    page.element(css="input[label='Customer']").input(CUSTOMER)
    page.button(value="Search").click()
    # The search returns one or more receipt records associated with GENERIC_CUSTOMER_01 from the lockbox import.
    page.element(css="table.search-results tbody tr").verify(V.like("*" + CUSTOMER + "*"))

    # Step 3: Click the receipt record linked to GENERIC_INVOICE_REF_01 to open the receipt detail view.
    # TODO: confirm with tx scan
    page.element(css="table.search-results tbody tr a.receipt-link").click()
    # The receipt detail page opens and displays the receipt header, applied amount, and application details.
    page.element(css="div.receipt-detail").verify(V.like("*Applications*"))

    # Step 4: Verify that the Applications section of the receipt detail shows GENERIC_INVOICE_REF_01 as an applied invoice.
    # GENERIC_INVOICE_REF_01 is listed in the Applications section with an applied amount equal to the receipt amount,
    # and the receipt status is 'Applied', confirming correct matching and application.
    page.element(css="div.applications-section").verify(V.like("*" + INVOICE_REF + "*"))

    # Step 5: Navigate to Manage Transactions and search for GENERIC_INVOICE_REF_01 to verify its updated balance.
    page.element(inner_text="Manage Transactions").click()
    # TODO: confirm with tx scan
    page.element(css="input[label='Transaction Number']").input(INVOICE_REF)
    page.button(value="Search").click()
    # GENERIC_INVOICE_REF_01 is displayed with a remaining balance of zero (or reduced by the receipt amount),
    # confirming the lockbox receipt has been correctly applied.
    page.element(css="td.remaining-balance").verify("0")
