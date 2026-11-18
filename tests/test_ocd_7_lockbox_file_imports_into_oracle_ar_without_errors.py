"""
Jira issue key : OCD-7
qTest test case: OCD-7 - Lockbox file imports into Oracle AR without errors
qTest ID       : 107945087
"""
import os
import pytest
from tbox_sdk import Secret, V

LOCKBOX_FILE = "GENERIC_LOCKBOX_FILE_01"
LOCKBOX_FORMAT = "GENERIC_LOCKBOX_FORMAT_01"


def test_lockbox_file_imports_into_oracle_ar_without_errors(tb) -> None:
    # Arrange – open application and sign in
    # Precondition: User is logged in with the Accounts Receivable Manager role (assumption).
    # A lockbox bank transmission file GENERIC_LOCKBOX_FILE_01 in format
    # GENERIC_LOCKBOX_FORMAT_01 is available and contains at least one receipt record.
    # A lockbox definition matching the file is configured in Oracle AR.
    tb.open(os.environ["ORACLE_URL"])
    page = tb.web
    page.textbox(id="userid").input(Secret.from_env("ORACLE_USER"))
    page.textbox(id="password").input(Secret.from_env("ORACLE_PASSWORD"))
    page.button(value="Sign In").click()

    # Step 1: Navigate to the AutoLockbox submission screen via Receivables > Receipts > Submit AutoLockbox
    # (assumption — exact path to be confirmed by story author).
    # TODO: confirm with tx scan
    page.element(inner_text="Receivables", index=1).click()
    page.element(inner_text="Receipts", index=1).click()
    page.element(inner_text="Submit AutoLockbox", index=1).click()
    # The Submit AutoLockbox screen is displayed.
    page.element(css="h1,h2", index=1).verify(V.like("*AutoLockbox*"))

    # Step 2: Enter the lockbox file path or upload file = GENERIC_LOCKBOX_FILE_01 in the data file field.
    # TODO: confirm with tx scan
    page.textbox(id="DataFile").input(LOCKBOX_FILE)
    # The file GENERIC_LOCKBOX_FILE_01 is accepted and the submission form is populated.
    page.textbox(id="DataFile").verify(LOCKBOX_FILE)

    # Step 3: Select the transmission format = GENERIC_LOCKBOX_FORMAT_01 for the import.
    # TODO: confirm with tx scan
    page.textbox(id="TransmissionFormat").input(LOCKBOX_FORMAT)
    # The transmission format GENERIC_LOCKBOX_FORMAT_01 is selected.
    page.textbox(id="TransmissionFormat").verify(LOCKBOX_FORMAT)

    # Step 4: Click Submit to initiate the AutoLockbox import process.
    page.button(value="Submit").click()
    # The process is submitted and a request ID is assigned.
    page.element(css="div.confirmation,span.request-id", index=1).verify(V.like("*request*"))

    # Step 5: Navigate to the Scheduled Processes screen and verify the status of the submitted AutoLockbox process.
    # TODO: confirm with tx scan
    page.element(inner_text="Scheduled Processes", index=1).click()
    page.textbox(id="processSearch").input("AutoLockbox")
    page.button(value="Search").click()
    # The AutoLockbox import process completes with a status of Completed and no error-level messages are present in the output log.
    page.element(css="td.process-status", index=1).verify("Completed")
