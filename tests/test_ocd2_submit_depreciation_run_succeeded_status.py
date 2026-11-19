"""
Jira issue: OCD-2
qTest test case: OCD-2 - User can submit a depreciation run for the current open period and have it reach a Succeeded status
qTest ID: 107947359
"""
import os
import pytest
from tbox_sdk import Secret, V

ASSET_BOOK = "GENERIC_ASSET_BOOK_01"
PERIOD = "GENERIC_PERIOD_01"


def test_submit_depreciation_run_succeeded_status(tb) -> None:
    # Precondition: User GENERIC_FA_USER_01 is logged in with the Fixed Assets Manager role.
    # Asset book GENERIC_ASSET_BOOK_01 exists and contains at least one capitalised, in-service asset.
    # Accounting period GENERIC_PERIOD_01 is open for the target ledger.
    # No prior depreciation run has been submitted for GENERIC_ASSET_BOOK_01 in GENERIC_PERIOD_01.

    # Arrange: open Oracle Fusion and sign in
    tb.open(os.environ["ORACLE_URL"])
    page = tb.web
    page.textbox(id="username").input(Secret.from_env("ORACLE_USER"))
    page.textbox(id="password").input(Secret.from_env("ORACLE_PASSWORD"))
    page.button(value="Sign In").click()

    # Step 1: Navigate to the depreciation submission screen within the Fixed Assets module.
    page.element(css="button.navigator-menu-icon").click()
    page.element(inner_text="Fixed Assets").click()
    page.element(inner_text="Depreciation").click()
    # The depreciation submission screen is displayed with entry fields for asset book and period.
    page.element(css="div.depreciation-submission-screen").verify(V.like("*Asset Book*"))

    # Step 2: Select GENERIC_ASSET_BOOK_01 in the Asset Book field on the depreciation submission screen.
    # TODO: confirm with tx scan
    page.element(css="input[label='Asset Book']").input(ASSET_BOOK)
    # GENERIC_ASSET_BOOK_01 is populated in the Asset Book field and the available periods for that book become selectable.
    page.element(css="input[label='Asset Book']").verify(ASSET_BOOK)

    # Step 3: Select GENERIC_PERIOD_01 in the Period field on the depreciation submission screen.
    # TODO: confirm with tx scan
    page.element(css="input[label='Period']").input(PERIOD)
    # GENERIC_PERIOD_01 is populated in the Period field.
    page.element(css="input[label='Period']").verify(PERIOD)

    # Step 4: Click the Submit button on the depreciation submission screen.
    page.button(value="Submit").click()
    # A confirmation message is displayed indicating the depreciation process has been submitted, along with a process ID or request number.
    page.element(css="div.confirmation-message").verify(V.like("*submitted*"))

    # Step 5: Navigate to Scheduled Processes and locate the submitted depreciation process by its process ID.
    page.element(css="button.navigator-menu-icon").click()
    page.element(inner_text="Scheduled Processes").click()
    # The process record is visible in Scheduled Processes and its Status field displays 'Succeeded' once processing is complete.
    page.element(css="td.process-status").verify("Succeeded")
