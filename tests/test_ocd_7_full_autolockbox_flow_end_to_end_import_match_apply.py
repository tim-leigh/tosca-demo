"""
Jira issue key : OCD-7
qTest test case: OCD-7 - Full AutoLockbox flow completes end-to-end: import, match, and apply
qTest ID       : 107945089
"""
import os
import pytest
from tbox_sdk import Secret, V

LOCKBOX_FILE = "GENERIC_LOCKBOX_FILE_02"
LOCKBOX_FORMAT = "GENERIC_LOCKBOX_FORMAT_01"
CUSTOMER_ACCT = "GENERIC_CUSTOMER_ACCT_02"
INVOICE_REF = "GENERIC_INVOICE_REF_AR_02"


def test_full_autolockbox_flow_end_to_end_import_match_apply(tb) -> None:
    # Arrange – open application and sign in
    # Precondition: User is logged in with the Accounts Receivable Manager role (assumption).
    # Lockbox file GENERIC_LOCKBOX_FILE_02 in format GENERIC_LOCKBOX_FORMAT_01 is available
    # and contains exactly one receipt that matches open invoice GENERIC_INVOICE_REF_AR_02 on
    # customer account GENERIC_CUSTOMER_ACCT_02. The lockbox definition is configured in Oracle AR.
    tb.open(os.environ["ORACLE_URL"])
    page = tb.web
    page.textbox(id="userid").input(Secret.from_env("ORACLE_USER"))
    page.textbox(id="password").input(Secret.from_env("ORACLE_PASSWORD"))
    page.button(value="Sign In").click()

    # Step 1: Navigate to the AutoLockbox submission screen and submit file = GENERIC_LOCKBOX_FILE_02
    # using format = GENERIC_LOCKBOX_FORMAT_01.
    # TODO: confirm with tx scan
    page.element(inner_text="Receivables", index=1).click()
    page.element(inner_text="Receipts", index=1).click()
    page.element(inner_text="Submit AutoLockbox", index=1).click()
    page.textbox(id="DataFile").input(LOCKBOX_FILE)
    page.textbox(id="TransmissionFormat").input(LOCKBOX_FORMAT)
    page.button(value="Submit").click()
    # The AutoLockbox process is submitted and assigned a request ID.
    page.element(css="div.confirmation,span.request-id", index=1).verify(V.like("*request*"))

    # Step 2: Navigate to the Scheduled Processes screen and verify the status of the AutoLockbox process for GENERIC_LOCKBOX_FILE_02.
    # TODO: confirm with tx scan
    page.element(inner_text="Scheduled Processes", index=1).click()
    page.textbox(id="processSearch").input("AutoLockbox")
    page.button(value="Search").click()
    # The process completes with status Completed and no error-level messages.
    page.element(css="td.process-status", index=1).verify("Completed")

    # Step 3: Navigate to Manage Receipts and search for the receipt created from GENERIC_LOCKBOX_FILE_02
    # for customer account = GENERIC_CUSTOMER_ACCT_02.
    # TODO: confirm with tx scan
    page.element(inner_text="Receivables", index=1).click()
    page.element(inner_text="Receipts", index=1).click()
    page.element(inner_text="Manage Receipts", index=1).click()
    page.textbox(id="CustomerAccount").input(CUSTOMER_ACCT)
    page.button(value="Search").click()
    # The receipt is listed and shows a status indicating it has been applied.
    page.element(css="td.receipt-status", index=1).verify(V.like("*Applied*"))

    # Step 4: Open the receipt and verify it is applied to invoice = GENERIC_INVOICE_REF_AR_02.
    # TODO: confirm with tx scan
    page.element(css="table.results tr.receipt-row", index=1).click()
    # The receipt application record shows GENERIC_INVOICE_REF_AR_02 with the full receipt amount
    # applied and a reduced or zero open balance on the invoice.
    page.element(css="td.applied-invoice,div.application-details", index=1).verify(V.like("*" + INVOICE_REF + "*"))
