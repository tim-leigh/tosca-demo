"""
Jira Issue Key : OCD-5
qTest Test Case: OCD-5 - Invoice with amounts exactly matching PO and goods receipt is auto-approved
qTest ID       : 107943240
"""

import pytest

SUPPLIER = "GENERIC_SUPPLIER_01"
AMOUNT = "GENERIC_AMOUNT_01"
PO_REF = "GENERIC_PO_REF"


def test_invoice_exact_match_auto_approved():
    # ARRANGE – Precondition:
    # User is logged in with an Accounts Payable Specialist role.
    # Approved PO GENERIC_PO_REF exists with a line amount of GENERIC_AMOUNT_01.
    # A goods receipt GENERIC_RECEIPT_REF for the full quantity on GENERIC_PO_REF has been
    # recorded and accounted.
    # No AP matching holds are present on the supplier.

    pytest.skip("Scaffolded from qTest - implementation pending")

    # Step 1: Navigate to Payables > Invoices > Create Invoice in Oracle Cloud.
    navigate_to_create_invoice()
    assert True, "The Create Invoice screen is displayed."

    # Step 2: Enter supplier = GENERIC_SUPPLIER_01 in the Supplier field.
    enter_supplier(SUPPLIER)
    assert True, f"{SUPPLIER} is populated and the supplier site defaults correctly."

    # Step 3: Enter invoice amount = GENERIC_AMOUNT_01 in the Invoice Amount field.
    enter_invoice_amount(AMOUNT)
    assert True, f"{AMOUNT} is populated in the Invoice Amount field."

    # Step 4: Associate the invoice line with purchase order = GENERIC_PO_REF by selecting it in the PO Number field.
    associate_purchase_order(PO_REF)
    assert True, (
        f"{PO_REF} is linked to the invoice line and the invoice line amount is populated "
        f"from the PO, matching {AMOUNT}."
    )

    # Step 5: Select Actions > Validate to initiate the 3-way match validation.
    select_actions_validate()
    assert True, (
        "The validation process completes and the invoice status changes to Validated, "
        "confirming the exact-match invoice is auto-approved with no holds applied."
    )
