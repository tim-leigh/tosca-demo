"""
Jira Issue Key : OCD-2
qTest Test Case: OCD-2 - Depreciation journals are created in General Ledger after a successful depreciation run
qTest ID       : 107945209
"""
import os
import pytest
from tbox_sdk import Secret, V

ACCOUNTING_PERIOD = "2026-01-01"
JOURNAL_SOURCE = "Fixed Assets"
ASSET_BOOK = "GENERIC_ASSET_BOOK_01"
LEDGER = "GENERIC_LEDGER_01"


def test_depreciation_journals_created_in_gl(tb) -> None:
    # Arrange — open application and sign in
    tb.open(os.environ["ORACLE_URL"])
    page = tb.web
    page.textbox(id="username").input(Secret.from_env("ORACLE_USER"))
    page.textbox(id="password").input(Secret.from_env("ORACLE_PASSWORD"))
    page.button(value="Sign In").click()

    # Precondition: The depreciation run for asset book = GENERIC_ASSET_BOOK_01 and period = 2026-01-01
    # has completed with status 'Succeeded'.
    # The user has access to the General Ledger Manage Journals screen.
    # Ledger = GENERIC_LEDGER_01.

    pytest.skip("Scaffolded from qTest - implementation pending")

    # Step 1: Navigate to the General Ledger module from the Oracle Cloud home page.
    page.element(inner_text="General Ledger").click()
    # Expected: The General Ledger module home page is displayed.
    # TODO: confirm with tx scan
    page.element(css="div.gl-home").verify(V.like("*General Ledger*"))

    # Step 2: Navigate to the Manage Journals screen within General Ledger.
    page.element(inner_text="Manage Journals").click()
    # Expected: The Manage Journals search screen is displayed.
    # TODO: confirm with tx scan
    page.element(css="div.manage-journals").verify(V.like("*Manage Journals*"))

    # Step 3: Enter accounting period = 2026-01-01 and journal source = Fixed Assets in the search filters,
    # then click Search.
    # TODO: confirm with tx scan
    page.element(css="input[id*='AccountingPeriod']").input(ACCOUNTING_PERIOD)
    page.element(css="input[id*='JournalSource']").input(JOURNAL_SOURCE)
    page.button(value="Search").click()
    # Expected: The search returns one or more journal entries sourced from Fixed Assets for the specified period.
    # TODO: confirm with tx scan
    page.element(css="td.journal-source").verify(JOURNAL_SOURCE)

    # Step 4: Verify that the returned journal entries include depreciation expense lines for
    # asset book = GENERIC_ASSET_BOOK_01.
    # Expected: Depreciation journal entries are present, showing debit and credit lines for the depreciation
    # expense and accumulated depreciation accounts associated with GENERIC_ASSET_BOOK_01.
    # TODO: confirm with tx scan
    page.element(css="td.journal-description").verify(V.like("*" + ASSET_BOOK + "*"))
