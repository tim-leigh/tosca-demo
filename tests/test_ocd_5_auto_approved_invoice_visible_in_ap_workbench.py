"""
Jira Issue Key : OCD-5
qTest Test Case: OCD-5 - Auto-approved invoice and its match details are visible in the AP workbench
qTest ID       : 107943236
"""

import pytest

INVOICE_REF = "GENERIC_INVOICE_REF"
PO_REF = "GENERIC_PO_REF"
RECEIPT_REF = "GENERIC_RECEIPT_REF"


def test_auto_approved_invoice_visible_in_ap_workbench():
    # ARRANGE – Precondition:
    # User is logged in with an Accounts Payable Specialist role.
    # AP invoice GENERIC_INVOICE_REF has been validated and auto-approved via 3-way match
    # against GENERIC_PO_REF and GENERIC_RECEIPT_REF.

    pytest.skip("Scaffolded from qTest - implementation pending")

    # Step 1: Navigate to Payables > Invoices > Manage Invoices in Oracle Cloud.
    navigate_to_manage_invoices()
    assert True, "The Manage Invoices (AP workbench) screen is displayed."

    # Step 2: Search for invoice number = GENERIC_INVOICE_REF in the Invoice Number search field.
    search_invoice(INVOICE_REF)
    assert True, f"Invoice {INVOICE_REF} is returned in the search results."

    # Step 3: Select GENERIC_INVOICE_REF to open the invoice detail view.
    open_invoice(INVOICE_REF)
    assert True, f"The invoice detail screen for {INVOICE_REF} is displayed."

    # Step 4: Verify the invoice status displayed in the Status field.
    verify_invoice_status(INVOICE_REF)
    assert True, "The invoice status shows Validated, confirming the auto-approval is reflected in the workbench."

    # Step 5: Navigate to the invoice line detail and verify that matched PO reference = GENERIC_PO_REF
    #         and receipt reference = GENERIC_RECEIPT_REF are visible.
    verify_match_references(PO_REF, RECEIPT_REF)
    assert True, (
        f"The invoice line displays {PO_REF} and {RECEIPT_REF} as matched references, confirming "
        "the 3-way match details are recorded and visible in the AP workbench."
    )
