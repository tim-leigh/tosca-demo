"""
Jira issue: OCD-7
qTest test case: OCD-7 - Lockbox file imports into Oracle Cloud AR without errors
qTest ID: 107947363
"""
import os
import pytest
from tbox_sdk import Secret, V

BANK_ACCOUNT = "GENERIC_BANK_ACCOUNT_01"
LOCKBOX_FILE = "GENERIC_LOCKBOX_FILE_01"


def test_lockbox_file_imports_without_errors(tb) -> None:
    # Precondition: User GENERIC_AR_USER_01 is logged in with the Accounts Receivable Specialist role.
    # A valid lockbox transmission file GENERIC_LOCKBOX_FILE_01 in format GENERIC_LOCKBOX_FORMAT_01
    # has been prepared and is available for upload.
    # A lockbox bank account GENERIC_BANK_ACCOUNT_01 is configured in Oracle Cloud AR.
    # At least one open customer invoice exists against customer GENERIC_CUSTOMER_01.

    # Arrange: open Oracle Cloud and sign in
    tb.open(os.environ["ORACLE_URL"])
    page = tb.web
    page.textbox(id="username").input(Secret.from_env("ORACLE_USER"))
    page.textbox(id="password").input(Secret.from_env("ORACLE_PASSWORD"))
    page.button(value="Sign In").click()

    # Step 1: Navigate to the Accounts Receivable module from the Oracle Cloud home page.
    page.element(css="button.navigator-menu-icon").click()
    page.element(inner_text="Accounts Receivable").click()
    # The Accounts Receivable module landing page opens without errors.
    page.element(css="div.module-landing-page").verify(V.like("*Accounts Receivable*"))

    # Step 2: Navigate to the Lockbox or Import Receipts submission screen within the Accounts Receivable module.
    page.element(inner_text="Import Receipts").click()
    # The lockbox submission screen is displayed with fields for bank account, file, and transmission parameters.
    page.element(css="div.lockbox-submission-screen").verify(V.like("*Bank Account*"))

    # Step 3: Select GENERIC_BANK_ACCOUNT_01 in the Bank Account field on the lockbox submission screen.
    # TODO: confirm with tx scan
    page.element(css="input[label='Bank Account']").input(BANK_ACCOUNT)
    # GENERIC_BANK_ACCOUNT_01 is populated in the Bank Account field.
    page.element(css="input[label='Bank Account']").verify(BANK_ACCOUNT)

    # Step 4: Attach or specify GENERIC_LOCKBOX_FILE_01 in the file input field on the lockbox submission screen.
    # TODO: confirm with tx scan
    page.element(css="input[type='file']").input(LOCKBOX_FILE)
    # GENERIC_LOCKBOX_FILE_01 is accepted and its name or path is displayed in the file field.
    page.element(css="input[type='file']").verify(V.like("*" + LOCKBOX_FILE + "*"))

    # Step 5: Click Submit on the lockbox submission screen to initiate the import process.
    page.button(value="Submit").click()
    # A confirmation message is displayed indicating the lockbox process has been submitted, along with a process ID.
    page.element(css="div.confirmation-message").verify(V.like("*submitted*"))

    # Step 6: Navigate to Scheduled Processes and locate the lockbox import process by its process ID.
    page.element(css="button.navigator-menu-icon").click()
    page.element(inner_text="Scheduled Processes").click()
    # The process status displays 'Succeeded' and no error records are reported, confirming the lockbox file imported without errors.
    page.element(css="td.process-status").verify("Succeeded")
