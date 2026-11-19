"""
Jira issue: OCD-5
qTest test case: OCD-5 - Invoice amount outside tolerance is routed to the exception queue after 3-way match failure
qTest ID: 107947365
"""
import os
import pytest
from tbox_sdk import Secret, V

SUPPLIER_PO_REF_02 = "GENERIC_PO_REF_02"
OOT_AMOUNT = "GENERIC_OOT_AMOUNT_01"
RECEIPT_REF_02 = "GENERIC_RECEIPT_REF_02"
TOLERANCE = "GENERIC_TOLERANCE_01"
PO_AMOUNT_02 = "GENERIC_PO_AMOUNT_02"


def test_invoice_outside_tolerance_exception_queue(tb) -> None:
    # Precondition: User GENERIC_AP_USER_01 is logged in with the Accounts Payable Specialist role.
    # A purchase order GENERIC_PO_REF_02 exists in Approved status with a line amount of GENERIC_PO_AMOUNT_02.
    # A goods receipt GENERIC_RECEIPT_REF_02 exists matched to GENERIC_PO_REF_02.
    # The invoice amount GENERIC_OOT_AMOUNT_01 is set to a value that exceeds GENERIC_TOLERANCE_01 relative to GENERIC_PO_AMOUNT_02.

    # Arrange: open Oracle Cloud and sign in
    tb.open(os.environ["ORACLE_URL"])
    page = tb.web
    page.textbox(id="username").input(Secret.from_env("ORACLE_USER"))
    page.textbox(id="password").input(Secret.from_env("ORACLE_PASSWORD"))
    page.button(value="Sign In").click()

    # Step 1: Navigate to the Invoices workbench in Oracle Cloud Accounts Payable.
    page.element(css="button.navigator-menu-icon").click()
    page.element(inner_text="Invoices").click()
    # The Invoices workbench opens and displays the invoice entry interface.
    page.element(css="div.invoices-workbench").verify(V.like("*Invoices*"))

    # Step 2: Click Create Invoice on the Invoices workbench to open a new invoice form.
    page.button(value="Create Invoice").click()
    # A new blank invoice form is displayed.
    page.element(css="div.invoice-form").verify(V.like("*Supplier*"))

    # Step 3: Enter the supplier associated with GENERIC_PO_REF_02 in the Supplier field on the invoice form.
    # TODO: confirm with tx scan
    page.element(css="input[label='Supplier']").input(SUPPLIER_PO_REF_02)
    # The supplier name is populated on the invoice form.
    page.element(css="input[label='Supplier']").verify(V.like("*" + SUPPLIER_PO_REF_02 + "*"))

    # Step 4: Enter GENERIC_OOT_AMOUNT_01 in the Invoice Amount field on the invoice form.
    # TODO: confirm with tx scan
    page.element(css="input[label='Invoice Amount']").input(OOT_AMOUNT)
    # GENERIC_OOT_AMOUNT_01 is accepted and displayed in the Invoice Amount field.
    page.element(css="input[label='Invoice Amount']").verify(OOT_AMOUNT)

    # Step 5: Navigate to the invoice lines section and enter GENERIC_PO_REF_02 in the Purchase Order field to associate the PO.
    # TODO: confirm with tx scan
    page.element(css="input[label='Purchase Order']").input(SUPPLIER_PO_REF_02)
    # The system retrieves and populates the PO line details from GENERIC_PO_REF_02 and links GENERIC_RECEIPT_REF_02.
    page.element(css="div.invoice-lines").verify(V.like("*" + RECEIPT_REF_02 + "*"))

    # Step 6: Click Validate on the invoice form to trigger the 3-way match process.
    page.button(value="Validate").click()
    # The validation applies a match hold to the invoice, the invoice status does not reach 'Approved',
    # and the invoice is visible in the exception queue with a hold reason indicating a tolerance mismatch.
    page.element(css="span.invoice-status").verify(V.like("*Hold*"))
