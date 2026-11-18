"""
Jira issue key : OCD-2
qTest test case: OCD-2 - User can submit a depreciation run for an open period
qTest ID       : 107945080
"""
import os
import pytest
from tbox_sdk import Secret, V

ASSET_BOOK = "GENERIC_ASSET_BOOK_01"
PERIOD = "GENERIC_PERIOD_01"


def test_submit_depreciation_run_for_open_period(tb) -> None:
    # Arrange – open application and sign in
    # Precondition: User is logged in with the Fixed Assets Manager role.
    # The Run Depreciation screen is open. Asset book GENERIC_ASSET_BOOK_01 exists and
    # contains at least one depreciable asset. Depreciation period GENERIC_PERIOD_01 is
    # open and has not yet been depreciated for this book.
    tb.open(os.environ["ORACLE_URL"])
    page = tb.web
    page.textbox(id="userid").input(Secret.from_env("ORACLE_USER"))
    page.textbox(id="password").input(Secret.from_env("ORACLE_PASSWORD"))
    page.button(value="Sign In").click()

    # Navigate to Run Depreciation screen (precondition fulfilment)
    # TODO: confirm with tx scan
    page.element(css="a.fa-work-area", index=1).click()
    page.element(inner_text="Depreciation", index=1).click()
    page.element(inner_text="Run Depreciation", index=1).click()

    # Step 1: Select the asset book = GENERIC_ASSET_BOOK_01 in the Book field on the Run Depreciation screen.
    # TODO: confirm with tx scan
    page.textbox(id="BookName").input(ASSET_BOOK)
    # The asset book GENERIC_ASSET_BOOK_01 is selected and the Period field is populated or becomes selectable.
    page.textbox(id="BookName").verify(ASSET_BOOK)

    # Step 2: Select the depreciation period = GENERIC_PERIOD_01 in the Period field.
    # TODO: confirm with tx scan
    page.textbox(id="PeriodName").input(PERIOD)
    # The period GENERIC_PERIOD_01 is selected and the form is ready for submission.
    page.textbox(id="PeriodName").verify(PERIOD)

    # Step 3: Click the Submit button to initiate the depreciation run.
    page.button(value="Submit").click()
    # The system accepts the submission, assigns a process request ID, and displays a confirmation or process monitor link.
    page.element(css="div.confirmation,div.process-id", index=1).verify(V.like("*request*"))
