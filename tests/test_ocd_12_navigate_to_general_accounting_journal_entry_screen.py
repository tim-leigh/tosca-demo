"""
Jira issue key : OCD-12
qTest test case: OCD-12 - User can navigate to the General Accounting Journal Entry screen from the home page
qTest ID       : 107945091
"""
import os
import pytest
from tbox_sdk import Secret, V


def test_navigate_to_general_accounting_journal_entry_screen(tb) -> None:
    # Arrange – open application and sign in
    # Precondition: User is logged in to Oracle Cloud with the General Accounting Manager role.
    # The Oracle Cloud home page is displayed.
    tb.open(os.environ["ORACLE_URL"])
    page = tb.web
    page.textbox(id="userid").input(Secret.from_env("ORACLE_USER"))
    page.textbox(id="password").input(Secret.from_env("ORACLE_PASSWORD"))
    page.button(value="Sign In").click()

    # Step 1: Locate and click the General Accounting work area icon or link on the Oracle Cloud home page.
    # TODO: confirm with tx scan
    page.element(inner_text="General Accounting", index=1).click()
    # The General Accounting work area or its task panel opens.
    page.element(css="div.task-panel,div.work-area", index=1).verify(V.like("*General Accounting*"))

    # Step 2: Select the Journals task from the General Accounting task panel.
    # TODO: confirm with tx scan
    page.element(inner_text="Journals", index=1).click()
    # The Journals task options are displayed, including an option to create a new journal entry.
    page.element(css="div.journal-tasks,ul.task-list", index=1).verify(V.like("*Create Journal*"))

    # Step 3: Click the Create Journal or equivalent link to open the journal entry screen.
    page.element(inner_text="Create Journal", index=1).click()
    # The General Accounting Journal Entry (journal batch creation) screen is displayed and ready for input.
    page.element(css="h1,h2", index=1).verify(V.like("*Create Journal*"))
