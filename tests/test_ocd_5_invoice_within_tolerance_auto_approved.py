"""
Jira Issue Key : OCD-5
qTest Test Case: OCD-5 - Invoice with amounts within the configured tolerance threshold is auto-approved
qTest ID       : 107943244
"""

import pytest

SUPPLIER = "GENERIC_SUPPLIER_01"
AMOUNT = "GENERIC_AMOUNT_01"
WITHIN_TOLERANCE_AMOUNT = "GENERIC_WITHIN_TOLERANCE_AMOUNT"
PO_REF = "GENERIC_PO_REF"


def test_invoice_within_tolerance_auto_approved():
    # ARRANGE – Precondition:
    # User is logged in with an Accounts Payable Specialist role.
    # Approved PO GENERIC_PO_REF exists with a line amount of GENERIC_AMOUNT_01.
    # Goods receipt GENERIC_RECEIPT_REF for the full quantity on GENERIC_PO_REF exists.
    # The AP matching tolerance is configured and active in Oracle for the relevant business unit.

    pytest.skip("Scaffolded from qTest - implementation pending")

    # Step 1: Navigate to Payables > Invoices > Create Invoice in Oracle Cloud.
    navigate_to_create_invoice()
    assert True, "The Create Invoice screen is displayed."

    # Step 2: Enter supplier = GENERIC_SUPPLIER_01 in the Supplier field.
    enter_supplier(SUPPLIER)
    assert True, f"{SUPPLIER} is populated and the supplier site defaults correctly."

    # Step 3: Enter invoice amount = GENERIC_WITHIN_TOLERANCE_AMOUNT in the Invoice Amount field,
    #         representing a value within the configured tolerance above GENERIC_AMOUNT_01.
    enter_invoice_amount(WITHIN_TOLERANCE_AMOUNT)
    assert True, f"{WITHIN_TOLERANCE_AMOUNT} is populated in the Invoice Amount field."

    # Step 4: Associate the invoice line with purchase order = GENERIC_PO_REF in the PO Number field.
    associate_purchase_order(PO_REF)
    assert True, f"{PO_REF} is linked to the invoice line."

    # Step 5: Select Actions > Validate to initiate 3-way match validation.
    select_actions_validate()
    assert True, (
        "The validation completes and the invoice status changes to Validated, confirming the "
        "within-tolerance variance does not trigger an exception hold and the invoice is auto-approved."
    )
