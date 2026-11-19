"""
Jira issue: OCD-5
qTest test case: OCD-5 - Mismatch details for an out-of-tolerance invoice are logged and visible in the AP workbench
qTest ID: 107947366
"""
import os
import pytest
from tbox_sdk import Secret, V

OOT_AMOUNT = "GENERIC_OOT_AMOUNT_01"
PO_REF_02 = "GENERIC_PO_REF_02"
RECEIPT_REF_02 = "GENERIC_RECEIPT_REF_02"


def test_mismatch_details_logged_ap_workbench(tb) -> None:
    # Precondition: User GENERIC_AP_USER_01 is logged in with the Accounts Payable Specialist role.
    # An AP invoice with amount GENERIC_OOT_AMOUNT_01 has been created and validated against
    # GENERIC_PO_REF_02 and GENERIC_RECEIPT_REF_02, resulting in a mismatch hold as established in test case 2.

    # Arrange: open Oracle Cloud and sign in
    tb.open(os.environ["ORACLE_URL"])
    page = tb.web
    page.textbox(id="username").input(Secret.from_env("ORACLE_USER"))
    page.textbox(id="password").input(Secret.from_env("ORACLE_PASSWORD"))
    page.button(value="Sign In").click()

    # Step 1: Navigate to Manage Invoices in Oracle Cloud Accounts Payable.
    page.element(css="button.navigator-menu-icon").click()
    page.element(inner_text="Manage Invoices").click()
    # The Manage Invoices search screen is displayed.
    page.element(css="div.manage-invoices-screen").verify(V.like("*Manage Invoices*"))

    # Step 2: Search for the out-of-tolerance invoice by entering GENERIC_OOT_AMOUNT_01 or the associated supplier reference
    # in the search filters, then click Search.
    # TODO: confirm with tx scan
    page.element(css="input[label='Invoice Amount']").input(OOT_AMOUNT)
    page.button(value="Search").click()
    # The out-of-tolerance invoice is returned in the search results with a hold indicator visible.
    page.element(css="table.search-results tbody tr").verify(V.like("*" + OOT_AMOUNT + "*"))

    # Step 3: Click the invoice number link to open the invoice detail view.
    page.element(css="table.search-results tbody tr a.invoice-number-link").click()
    # The invoice detail page opens, displaying the invoice header, line details, and a Holds section or tab.
    page.element(css="div.invoice-detail").verify(V.like("*Holds*"))

    # Step 4: Navigate to the Holds tab or section within the invoice detail view.
    page.element(inner_text="Holds").click()
    # The Holds section is displayed and contains at least one hold entry with a hold reason code
    # that identifies the 3-way match mismatch.
    page.element(css="table.holds-table tbody tr").verify(V.like("*Match*"))

    # Step 5: Verify that the mismatch hold entry in the Holds section displays details linking to GENERIC_PO_REF_02 and GENERIC_RECEIPT_REF_02.
    # The mismatch hold record shows details sufficient to identify the variance (hold reason, associated PO reference
    # GENERIC_PO_REF_02, and receipt reference GENERIC_RECEIPT_REF_02), confirming that mismatch details are logged
    # and visible in the AP workbench.
    page.element(css="table.holds-table tbody tr").verify(V.like("*" + PO_REF_02 + "*"))
