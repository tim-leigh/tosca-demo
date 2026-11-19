"""
Jira issue: OCD-5
qTest test case: OCD-5 - Invoice amount within tolerance of PO and receipt is auto-approved via 3-way match
qTest ID: 107947369
"""
import os
import pytest
from tbox_sdk import Secret, V

SUPPLIER_PO_REF = "GENERIC_PO_REF_01"
INVOICE_AMOUNT = "GENERIC_INVOICE_AMOUNT_01"
TOLERANCE = "GENERIC_TOLERANCE_01"
PO_AMOUNT = "GENERIC_PO_AMOUNT_01"
RECEIPT_REF = "GENERIC_RECEIPT_REF_01"


def test_invoice_within_tolerance_auto_approved(tb) -> None:
    # Precondition: User GENERIC_AP_USER_01 is logged in with the Accounts Payable Specialist role.
    # A purchase order GENERIC_PO_REF_01 exists in Approved status with a line amount of GENERIC_PO_AMOUNT_01.
    # A goods receipt GENERIC_RECEIPT_REF_01 exists matched to GENERIC_PO_REF_01 for the full PO quantity.
    # The AP invoice amount GENERIC_INVOICE_AMOUNT_01 is set to a value within GENERIC_TOLERANCE_01 of GENERIC_PO_AMOUNT_01.
    # The supplier for the PO is configured in Oracle Cloud.

    # Arrange: open Oracle Cloud and sign in
    tb.open(os.environ["ORACLE_URL"])
    page = tb.web
    page.textbox(id="username").input(Secret.from_env("ORACLE_USER"))
    page.textbox(id="password").input(Secret.from_env("ORACLE_PASSWORD"))
    page.button(value="Sign In").click()

    # Step 1: Navigate to the Invoices workbench in Oracle Cloud Accounts Payable.
    page.element(css="button.navigator-menu-icon").click()
    page.element(inner_text="Invoices").click()
    # The Invoices workbench opens and displays the invoice entry and search interface.
    page.element(css="div.invoices-workbench").verify(V.like("*Invoices*"))

    # Step 2: Click Create Invoice on the Invoices workbench to open a new invoice form.
    page.button(value="Create Invoice").click()
    # A new blank invoice form is displayed with required header fields.
    page.element(css="div.invoice-form").verify(V.like("*Supplier*"))

    # Step 3: Enter the supplier associated with GENERIC_PO_REF_01 in the Supplier field on the invoice form.
    # TODO: confirm with tx scan
    page.element(css="input[label='Supplier']").input(SUPPLIER_PO_REF)
    # The supplier name is populated and the invoice form updates to reflect supplier-specific defaults.
    page.element(css="input[label='Supplier']").verify(V.like("*" + SUPPLIER_PO_REF + "*"))

    # Step 4: Enter GENERIC_INVOICE_AMOUNT_01 in the Invoice Amount field on the invoice form.
    # TODO: confirm with tx scan
    page.element(css="input[label='Invoice Amount']").input(INVOICE_AMOUNT)
    # GENERIC_INVOICE_AMOUNT_01 is accepted and displayed in the Invoice Amount field.
    page.element(css="input[label='Invoice Amount']").verify(INVOICE_AMOUNT)

    # Step 5: Navigate to the invoice lines section and enter GENERIC_PO_REF_01 in the Purchase Order field to associate the PO.
    # TODO: confirm with tx scan
    page.element(css="input[label='Purchase Order']").input(SUPPLIER_PO_REF)
    # The system retrieves and populates the PO line details from GENERIC_PO_REF_01, and the goods receipt GENERIC_RECEIPT_REF_01 is linked automatically.
    page.element(css="div.invoice-lines").verify(V.like("*" + RECEIPT_REF + "*"))

    # Step 6: Click Validate on the invoice form to trigger the 3-way match process.
    page.button(value="Validate").click()
    # The validation completes without holds being applied, and the invoice status changes to 'Approved',
    # confirming that the invoice amount is within GENERIC_TOLERANCE_01 of both GENERIC_PO_REF_01 and GENERIC_RECEIPT_REF_01.
    page.element(css="span.invoice-status").verify("Approved")
