"""
Jira issue key : OCD-5
qTest test case: OCD-5 - Full end-to-end 3-way match flow completes for a within-tolerance invoice
qTest ID       : 107945084
"""
import os
import pytest
from tbox_sdk import Secret, V

INVOICE_REF = "GENERIC_INVOICE_REF_03"
PO_REF = "GENERIC_PO_REF_03"
RECEIPT_REF = "GENERIC_RECEIPT_REF_03"
TOLERANCE = "GENERIC_TOLERANCE_01"


def test_full_end_to_end_3_way_match_flow_within_tolerance(tb) -> None:
    # Arrange – open application and sign in
    # Precondition: User is logged in with the Accounts Payable Manager role (assumption).
    # Approved PO GENERIC_PO_REF_03 exists. Goods receipt GENERIC_RECEIPT_REF_03 matched to
    # GENERIC_PO_REF_03 exists. Supplier invoice GENERIC_INVOICE_REF_03 exists with an amount
    # within GENERIC_TOLERANCE_01 of both the PO and receipt amounts.
    tb.open(os.environ["ORACLE_URL"])
    page = tb.web
    page.textbox(id="userid").input(Secret.from_env("ORACLE_USER"))
    page.textbox(id="password").input(Secret.from_env("ORACLE_PASSWORD"))
    page.button(value="Sign In").click()

    # Step 1: Navigate to Payables > Invoices > Manage Invoices.
    # TODO: confirm with tx scan
    page.element(inner_text="Payables", index=1).click()
    page.element(inner_text="Invoices", index=1).click()
    page.element(inner_text="Manage Invoices", index=1).click()
    # The Manage Invoices screen is displayed.
    page.element(css="h1,h2", index=1).verify(V.like("*Manage Invoices*"))

    # Step 2: Search for and open invoice = GENERIC_INVOICE_REF_03.
    # TODO: confirm with tx scan
    page.textbox(id="InvoiceNum").input(INVOICE_REF)
    page.button(value="Search").click()
    page.element(inner_text=INVOICE_REF, index=1).click()
    # Invoice GENERIC_INVOICE_REF_03 is displayed with its current pre-match status.
    page.element(css="div.invoice-header,h1,h2", index=1).verify(V.like("*" + INVOICE_REF + "*"))

    # Step 3: Initiate the 3-way match process for GENERIC_INVOICE_REF_03 against GENERIC_PO_REF_03 and GENERIC_RECEIPT_REF_03.
    # TODO: confirm with tx scan
    page.button(value="Match").click()
    # The match process runs and validates the invoice against the PO and receipt without routing to an exception queue.
    page.element(css="div.match-status", index=1).verify(V.like("*matched*"))

    # Step 4: Verify the final status of invoice GENERIC_INVOICE_REF_03 on the Manage Invoices screen.
    # TODO: confirm with tx scan
    page.element(inner_text="Manage Invoices", index=1).click()
    page.textbox(id="InvoiceNum").input(INVOICE_REF)
    page.button(value="Search").click()
    # Invoice GENERIC_INVOICE_REF_03 status displays as Approved (or Validated — story author to confirm
    # exact label), confirming the full end-to-end 3-way match flow completed successfully.
    page.element(css="td.invoice-status", index=1).verify(V.like("*Approved*"))
