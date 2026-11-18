"""
Jira issue key : OCD-5
qTest test case: OCD-5 - Invoice outside tolerance is routed to the AP exception queue
qTest ID       : 107945085
"""
import os
import pytest
from tbox_sdk import Secret, V

INVOICE_REF = "GENERIC_INVOICE_REF_02"
PO_REF = "GENERIC_PO_REF_02"
RECEIPT_REF = "GENERIC_RECEIPT_REF_02"
TOLERANCE = "GENERIC_TOLERANCE_01"


def test_invoice_outside_tolerance_routed_to_ap_exception_queue(tb) -> None:
    # Arrange – open application and sign in
    # Precondition: User is logged in with the Accounts Payable Manager role (assumption).
    # An approved purchase order GENERIC_PO_REF_02 exists. A goods receipt
    # GENERIC_RECEIPT_REF_02 matched to GENERIC_PO_REF_02 exists. A supplier invoice
    # GENERIC_INVOICE_REF_02 exists with an amount that exceeds GENERIC_TOLERANCE_01
    # relative to the PO or receipt amount.
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

    # Step 2: Search for invoice = GENERIC_INVOICE_REF_02 using the invoice number search field.
    # TODO: confirm with tx scan
    page.textbox(id="InvoiceNum").input(INVOICE_REF)
    page.button(value="Search").click()
    # Invoice GENERIC_INVOICE_REF_02 is returned in the search results.
    page.element(css="table.results td", index=1).verify(V.like("*" + INVOICE_REF + "*"))

    # Step 3: Select invoice GENERIC_INVOICE_REF_02 and trigger the matching process by clicking the Match button or equivalent action.
    # TODO: confirm with tx scan
    page.element(inner_text=INVOICE_REF, index=1).click()
    page.button(value="Match").click()
    # The system initiates the 3-way match process for GENERIC_INVOICE_REF_02 and detects the amount is outside tolerance.
    page.element(css="div.match-status,div.process-status", index=1).verify(V.like("*outside tolerance*"))

    # Step 4: Navigate to the AP exception queue (assumption: accessible via AP Workbench > Exceptions —
    # exact path to be confirmed by story author) and search for GENERIC_INVOICE_REF_02.
    # TODO: confirm with tx scan
    page.element(inner_text="AP Workbench", index=1).click()
    page.element(inner_text="Exceptions", index=1).click()
    page.textbox(id="InvoiceSearch").input(INVOICE_REF)
    page.button(value="Search").click()
    # Invoice GENERIC_INVOICE_REF_02 appears in the exception queue, confirming it was routed there rather than auto-approved.
    page.element(css="table.exception-queue td", index=1).verify(V.like("*" + INVOICE_REF + "*"))
