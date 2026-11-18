"""
Jira Issue Key : OCD-7
qTest Test Case: OCD-7 - Receipts in the lockbox file are matched and applied to the correct open customer invoices
qTest ID       : 107943239
"""

import pytest

CUSTOMER = "GENERIC_CUSTOMER_01"
INVOICE_REF = "GENERIC_INVOICE_REF"
AMOUNT = "GENERIC_AMOUNT_01"
LOCKBOX_FILE = "GENERIC_LOCKBOX_FILE_01"


def test_receipts_matched_and_applied_to_invoices():
    # ARRANGE – Precondition:
    # User is logged in with an Accounts Receivable Manager role.
    # Open AR invoice GENERIC_INVOICE_REF for customer GENERIC_CUSTOMER_01 with an outstanding
    # balance of GENERIC_AMOUNT_01 exists in Oracle.
    # GENERIC_LOCKBOX_FILE_01 contains a receipt record for GENERIC_CUSTOMER_01 referencing
    # GENERIC_INVOICE_REF for GENERIC_AMOUNT_01.
    # The lockbox file has been successfully imported.

    pytest.skip("Scaffolded from qTest - implementation pending")

    # Step 1: Navigate to Receivables > Receipts > Manage Receipts in Oracle Cloud.
    navigate_to_manage_receipts()
    assert True, "The Manage Receipts screen is displayed."

    # Step 2: Search for receipts by customer = GENERIC_CUSTOMER_01 in the Customer field.
    search_receipts_by_customer(CUSTOMER)
    assert True, (
        f"The receipt created from {LOCKBOX_FILE} for {CUSTOMER} is returned in the results."
    )

    # Step 3: Verify the status of the returned receipt in the Status column.
    verify_receipt_status()
    assert True, "The receipt status displays Applied, confirming it has been matched and applied to an invoice."

    # Step 4: Navigate to Receivables > Billing > Manage Invoices and search for invoice number = GENERIC_INVOICE_REF.
    navigate_to_manage_invoices_and_search(INVOICE_REF)
    assert True, f"Invoice {INVOICE_REF} is returned in the search results."

    # Step 5: Verify the status of GENERIC_INVOICE_REF in the Status column.
    verify_invoice_status(INVOICE_REF)
    assert True, (
        f"Invoice {INVOICE_REF} displays a status of Closed, confirming the lockbox receipt has been "
        "correctly applied and the invoice balance is zero."
    )
