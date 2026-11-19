"""
Jira issue: OCD-12
qTest test case: OCD-12 - User can navigate to the General Accounting Journal Entry screen from the home page
qTest ID: 107947367
"""
import os
import pytest
from tbox_sdk import Secret, V


def test_navigate_to_journal_entry_screen(tb) -> None:
    # Precondition: User GENERIC_GA_USER_01 is logged in to Oracle Cloud with the General Accounting Manager role.
    # A valid open accounting period exists in the target ledger.

    # Arrange: open Oracle Cloud and sign in
    tb.open(os.environ["ORACLE_URL"])
    page = tb.web
    page.textbox(id="username").input(Secret.from_env("ORACLE_USER"))
    page.textbox(id="password").input(Secret.from_env("ORACLE_PASSWORD"))
    page.button(value="Sign In").click()

    # Step 1: Navigate to the Oracle Cloud home page as GENERIC_GA_USER_01.
    # (Sign-in above lands on the home page.)
    # The Oracle Cloud home page is displayed and shows the infolets and Navigator icon appropriate for the General Accounting Manager role.
    page.element(css="div.home-page").verify(V.like("*Navigator*"))

    # Step 2: Click the Navigator menu icon on the Oracle Cloud home page.
    page.element(css="button.navigator-menu-icon").click()
    # The Navigator panel opens and displays the available application modules for GENERIC_GA_USER_01,
    # including a General Accounting or Journals option.
    page.element(css="div.navigator-panel").verify(V.like("*General Accounting*"))

    # Step 3: Select General Accounting from the Navigator panel.
    page.element(inner_text="General Accounting").click()
    # The General Accounting work area opens and displays journal-related tasks or a Journals landing page.
    page.element(css="div.general-accounting-work-area").verify(V.like("*Journals*"))

    # Step 4: Click the Journals task or Create Journal link within the General Accounting work area.
    page.element(inner_text="Journals").click()
    # The General Accounting Journal Entry screen opens and displays the journal batch header and line entry form,
    # confirming the navigation path is accessible.
    page.element(css="div.journal-entry-screen").verify(V.like("*Journal Batch*"))
