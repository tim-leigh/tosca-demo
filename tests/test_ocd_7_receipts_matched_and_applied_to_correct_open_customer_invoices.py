"""
Jira issue key : OCD-7
qTest test case: OCD-7 - Receipts from the lockbox file are matched and applied to the correct open customer invoices
qTest ID       : 107945090
"""
import os
import pytest
from tbox_sdk import Secret, V

CUSTOMER_ACCT = "GENERIC_CUSTOMER_ACCT_01"
INVOICE_REF = "GENERIC_INVOICE_REF_AR_01"
LOCKBOX_FILE = "GENERIC_LOCKBOX_FILE_01"


def test_receipts_matched_and_applied_to_correct_open_customer_invoices(tb) -> None:
    # Arrange – open application and sign in
    # Precondition: User is logged in with the Accounts Receivable Manager role (assumption).
    # AutoLockbox import of GENERIC_LOCKBOX_FILE_01 has completed successfully.
    # Customer account GENERIC_CUSTOMER_ACCT_01 exists with open invoice GENERIC_INVOICE_REF_AR_01.
    # The lockbox file contains a receipt record whose reference number matches GENERIC_INVOICE_REF_AR_01.
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

    # Step 2: Search for receipts associated with customer account = GENERIC_CUSTOMER_ACCT_01 that were created by the lockbox import.
    # TODO: confirm with tx scan
    page.textbox(id="CustomerAccount").input(CUSTOMER_ACCT)
    page.button(value="Search").click()
    # The receipt created from GENERIC_LOCKBOX_FILE_01 for GENERIC_CUSTOMER_ACCT_01 is listed.
    page.element(css="table.results td", index=1).verify(V.like("*" + CUSTOMER_ACCT + "*"))

    # Step 3: Open the receipt record and verify the application details.
    # TODO: confirm with tx scan
    page.element(css="table.results tr.receipt-row", index=1).click()
    # The receipt is applied to invoice GENERIC_INVOICE_REF_AR_01, the applied amount equals the receipt amount,
    # and the invoice balance is reduced accordingly.
    page.element(css="td.applied-invoice,div.application-details", index=1).verify(V.like("*" + INVOICE_REF + "*"))
