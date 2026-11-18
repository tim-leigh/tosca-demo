"""
Jira issue key : OCD-2
qTest test case: OCD-2 - Depreciation run completes with a Completed status
qTest ID       : 107945079
"""
import os
import pytest
from tbox_sdk import Secret, V

ASSET_BOOK = "GENERIC_ASSET_BOOK_01"
PERIOD = "GENERIC_PERIOD_01"


def test_depreciation_run_completes_with_completed_status(tb) -> None:
    # Arrange – open application and sign in
    # Precondition: User is logged in with the Fixed Assets Manager role. A depreciation
    # run for asset book GENERIC_ASSET_BOOK_01 and period GENERIC_PERIOD_01 has been
    # submitted and a process request ID has been assigned.
    tb.open(os.environ["ORACLE_URL"])
    page = tb.web
    page.textbox(id="userid").input(Secret.from_env("ORACLE_USER"))
    page.textbox(id="password").input(Secret.from_env("ORACLE_PASSWORD"))
    page.button(value="Sign In").click()

    # Step 1: Navigate to the Scheduled Processes screen from the Tools menu or the process confirmation link.
    # TODO: confirm with tx scan
    page.element(inner_text="Scheduled Processes", index=1).click()
    # The Scheduled Processes screen opens and the submitted depreciation run is listed.
    page.element(css="h1,h2", index=1).verify(V.like("*Scheduled Processes*"))

    # Step 2: Locate the depreciation run process for asset book = GENERIC_ASSET_BOOK_01 and period = GENERIC_PERIOD_01 in the process list.
    # TODO: confirm with tx scan
    page.textbox(id="processSearch").input(ASSET_BOOK)
    page.button(value="Search").click()
    # The depreciation run process entry is visible in the list with its request ID.
    page.element(css="table.process-list td", index=1).verify(V.like("*" + ASSET_BOOK + "*"))

    # Step 3: Verify the status of the located depreciation run process.
    # TODO: confirm with tx scan
    # The process status displays as Completed with no error indicators
    # (assumption: 'Completed' is the expected success status; story author to confirm).
    page.element(css="table.process-list td.status", index=1).verify("Completed")
