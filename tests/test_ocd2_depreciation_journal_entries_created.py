"""
Jira issue: OCD-2
qTest test case: OCD-2 - Depreciation journal entries are created in the ledger after a successful depreciation run
qTest ID: 107947362
"""
import os
import pytest
from tbox_sdk import Secret, V

ASSET_BOOK = "GENERIC_ASSET_BOOK_01"
PERIOD = "GENERIC_PERIOD_01"


def test_depreciation_journal_entries_created(tb) -> None:
    # Precondition: A depreciation run for asset book GENERIC_ASSET_BOOK_01 and period GENERIC_PERIOD_01
    # has completed with a status of 'Succeeded'. User GENERIC_FA_USER_01 has access to both
    # the Fixed Assets module and the General Ledger module.

    # Arrange: open Oracle Fusion and sign in
    tb.open(os.environ["ORACLE_URL"])
    page = tb.web
    page.textbox(id="username").input(Secret.from_env("ORACLE_USER"))
    page.textbox(id="password").input(Secret.from_env("ORACLE_PASSWORD"))
    page.button(value="Sign In").click()

    # Step 1: Navigate to the General Ledger module from the Oracle Fusion Navigator menu.
    page.element(css="button.navigator-menu-icon").click()
    page.element(inner_text="General Ledger").click()
    # The General Ledger module landing page opens without errors.
    page.element(css="div.module-landing-page").verify(V.like("*General Ledger*"))

    # Step 2: Navigate to Manage Journals within the General Ledger module.
    page.element(inner_text="Manage Journals").click()
    # The Manage Journals search screen is displayed.
    page.element(css="div.manage-journals-screen").verify(V.like("*Manage Journals*"))

    # Step 3: Enter GENERIC_PERIOD_01 in the Accounting Period filter field on the Manage Journals search screen.
    # TODO: confirm with tx scan
    page.element(css="input[label='Accounting Period']").input(PERIOD)
    # GENERIC_PERIOD_01 is populated in the filter field.
    page.element(css="input[label='Accounting Period']").verify(PERIOD)

    # Step 4: Select Assets in the Journal Source filter field on the Manage Journals search screen, then click Search.
    # TODO: confirm with tx scan
    page.element(css="input[label='Journal Source']").input("Assets")
    page.button(value="Search").click()
    # The search executes and returns a list of journal entries sourced from Assets for GENERIC_PERIOD_01.
    page.element(css="table.search-results tbody tr").verify(V.like("*Assets*"))

    # Step 5: Verify that at least one journal entry in the results is associated with GENERIC_ASSET_BOOK_01 and GENERIC_PERIOD_01.
    # One or more depreciation journal entries are listed with the source 'Assets', the correct period GENERIC_PERIOD_01,
    # and a status of 'Posted' or 'Created', confirming that the depreciation run generated journal entries.
    page.element(css="table.search-results tbody tr").verify(V.like("*" + ASSET_BOOK + "*"))
