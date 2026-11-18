"""
Jira issue key : OCD-5
qTest test case: OCD-5 - Invoice within tolerance of PO and receipt is auto-approved via 3-way match
qTest ID       : 107945083
"""
import os
import pytest
from tbox_sdk import Secret, V

INVOICE_REF = "GENERIC_INVOICE_REF_01"
PO_REF = "GENERIC_PO_REF_01"
RECEIPT_REF = "GENERIC_RECEIPT_REF_01"
TOLERANCE = "GENERIC_TOLERANCE_01"


def test_invoice_within_tolerance_auto_approved_via_3_way_match(tb) -> None:
    # Arrange – open application and sign in
    # Precondition: User is logged in with the Accounts Payable Manager role (assumption).
    # An approved purchase order GENERIC_PO_REF_01 exists. A goods receipt
    # GENERIC_RECEIPT_REF_01 matched to GENERIC_PO_REF_01 exists. A supplier invoice
    # GENERIC_INVOICE_REF_01 exists with an amount within GENERIC_TOLERANCE_01 of both
    # the PO and receipt amounts.
    tb.open(os.environ["ORACLE_URL"])
    page = tb.web
    page.textbox(id="userid").input(Secret.from_env("ORACLE_USER"))
    page.textbox(id="password").input(Secret.from_env("ORACLE_PASSWORD"))
    page.button(value="Sign In").click()

    # Step 1: Navigate to the Invoices work area via Payables > Invoices > Manage Invoices.
    # TODO: confirm with tx scan
    page.element(inner_text="Payables", index=1).click()
    page.element(inner_text="Invoices", index=1).click()
    page.element(inner_text="Manage Invoices", index=1).click()
    # The Manage Invoices screen is displayed.
    page.element(css="h1,h2", index=1).verify(V.like("*Manage Invoices*"))

    # Step 2: Search for invoice = GENERIC_INVOICE_REF_01 using the invoice number search field.
    # TODO: confirm with tx scan
    page.textbox(id="InvoiceNum").input(INVOICE_REF)
    page.button(value="Search").click()
    # Invoice GENERIC_INVOICE_REF_01 is returned in the search results.
    page.element(css="table.results td", index=1).verify(V.like("*" + INVOICE_REF + "*"))

    # Step 3: Select invoice GENERIC_INVOICE_REF_01 and trigger the matching process by clicking the Match button or equivalent action.
    # TODO: confirm with tx scan
    page.element(inner_text=INVOICE_REF, index=1).click()
    page.button(value="Match").click()
    # The system initiates the 3-way match process for GENERIC_INVOICE_REF_01 against GENERIC_PO_REF_01 and GENERIC_RECEIPT_REF_01.
    page.element(css="div.match-status,div.process-status", index=1).verify(V.like("*match*"))

    # Step 4: Verify the invoice status displayed for GENERIC_INVOICE_REF_01 after the match process completes.
    # TODO: confirm with tx scan
    # Invoice GENERIC_INVOICE_REF_01 status shows as Approved (or Validated — exact label to be confirmed
    # by story author per quality finding F2), confirming auto-approval.
    page.element(css="td.invoice-status", index=1).verify(V.like("*Approved*"))
