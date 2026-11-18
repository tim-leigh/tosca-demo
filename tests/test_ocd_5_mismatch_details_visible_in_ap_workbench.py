"""
Jira issue key : OCD-5
qTest test case: OCD-5 - Mismatch details for an out-of-tolerance invoice are visible in the AP workbench
qTest ID       : 107945086
"""
import os
import pytest
from tbox_sdk import Secret, V

INVOICE_REF = "GENERIC_INVOICE_REF_02"
TOLERANCE = "GENERIC_TOLERANCE_01"


def test_mismatch_details_visible_in_ap_workbench(tb) -> None:
    # Arrange – open application and sign in
    # Precondition: User is logged in with the Accounts Payable Manager role (assumption).
    # Invoice GENERIC_INVOICE_REF_02 has already been processed through the 3-way match
    # and routed to the exception queue due to an amount outside GENERIC_TOLERANCE_01.
    tb.open(os.environ["ORACLE_URL"])
    page = tb.web
    page.textbox(id="userid").input(Secret.from_env("ORACLE_USER"))
    page.textbox(id="password").input(Secret.from_env("ORACLE_PASSWORD"))
    page.button(value="Sign In").click()

    # Step 1: Navigate to the AP Workbench from the Payables work area.
    # TODO: confirm with tx scan
    page.element(inner_text="Payables", index=1).click()
    page.element(inner_text="AP Workbench", index=1).click()
    # The AP Workbench screen is displayed.
    page.element(css="h1,h2", index=1).verify(V.like("*AP Workbench*"))

    # Step 2: Search for invoice = GENERIC_INVOICE_REF_02 within the AP Workbench.
    # TODO: confirm with tx scan
    page.textbox(id="InvoiceSearch").input(INVOICE_REF)
    page.button(value="Search").click()
    # Invoice GENERIC_INVOICE_REF_02 is located and its record is displayed.
    page.element(css="table.results td", index=1).verify(V.like("*" + INVOICE_REF + "*"))

    # Step 3: Open the mismatch or match details section for invoice GENERIC_INVOICE_REF_02.
    # TODO: confirm with tx scan
    page.element(inner_text=INVOICE_REF, index=1).click()
    page.element(inner_text="Match Details", index=1).click()
    # The mismatch details section is displayed, showing at minimum the PO amount, receipt amount,
    # invoice amount, and the calculated variance (assumption: these are the minimum required fields
    # per quality finding F4 — story author to confirm exact field list).
    page.element(css="div.mismatch-details,section.match-details", index=1).verify(V.like("*variance*"))
