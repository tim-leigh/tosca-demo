"""
Jira Issue Key : OCD-7
qTest Test Case: OCD-7 - Unmatched receipts in the lockbox file are flagged and available for manual review
qTest ID       : 107943238
"""

import pytest

CUSTOMER = "GENERIC_CUSTOMER_02"
LOCKBOX_FILE = "GENERIC_LOCKBOX_FILE_02"


def test_unmatched_receipts_flagged_for_manual_review():
    # ARRANGE – Precondition:
    # User is logged in with an Accounts Receivable Manager role.
    # GENERIC_LOCKBOX_FILE_02 contains at least one receipt record for customer GENERIC_CUSTOMER_02
    # with an invoice reference that does not match any open invoice in Oracle.
    # GENERIC_LOCKBOX_FILE_02 has been successfully imported.

    pytest.skip("Scaffolded from qTest - implementation pending")

    # Step 1: Navigate to Receivables > Receipts > Manage Receipts in Oracle Cloud.
    navigate_to_manage_receipts()
    assert True, "The Manage Receipts screen is displayed."

    # Step 2: Search for receipts by customer = GENERIC_CUSTOMER_02 in the Customer field.
    search_receipts_by_customer(CUSTOMER)
    assert True, (
        f"The unmatched receipt from {LOCKBOX_FILE} for {CUSTOMER} is returned in the results."
    )

    # Step 3: Verify the status of the returned unmatched receipt in the Status column.
    verify_receipt_status()
    assert True, "The receipt status displays Unapplied, indicating the system has flagged it as unmatched."

    # Step 4: Verify that the unmatched receipt is accessible from the Unapplied Receipts workbench
    #         or equivalent manual review queue.
    verify_receipt_in_manual_review_queue()
    assert True, (
        "The receipt appears in the manual review queue, confirming it has been correctly "
        "routed for manual follow-up action."
    )
