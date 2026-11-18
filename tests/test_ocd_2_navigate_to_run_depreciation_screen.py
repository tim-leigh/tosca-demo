"""
Jira issue key : OCD-2
qTest test case: OCD-2 - User can navigate to the Run Depreciation screen in Oracle Cloud Fixed Assets
qTest ID       : 107945078
"""
import os
import pytest
from tbox_sdk import Secret, V


def test_navigate_to_run_depreciation_screen(tb) -> None:
    # Arrange – open application and sign in
    # Precondition: User is logged in to Oracle Cloud with the Fixed Assets Manager role
    # (assumption: role name is GENERIC_FA_ROLE_01, to be confirmed by story author).
    # The Oracle Cloud home page is displayed.
    tb.open(os.environ["ORACLE_URL"])
    page = tb.web
    page.textbox(id="userid").input(Secret.from_env("ORACLE_USER"))
    page.textbox(id="password").input(Secret.from_env("ORACLE_PASSWORD"))
    page.button(value="Sign In").click()

    # Step 1: Navigate to the Fixed Assets work area from the Oracle Cloud home page.
    # TODO: confirm with tx scan
    page.element(css="a.fa-work-area", index=1).click()
    # The Fixed Assets work area opens and its task menu is visible.
    page.element(css="div.task-menu", index=1).verify(V.like("*Fixed Assets*"))

    # Step 2: Select the Depreciation option from the Fixed Assets task menu.
    # TODO: confirm with tx scan
    page.element(inner_text="Depreciation", index=1).click()
    # The Depreciation sub-menu or landing page is displayed.
    page.element(css="div.depreciation-menu", index=1).verify(V.like("*Depreciation*"))

    # Step 3: Click the Run Depreciation task link.
    page.element(inner_text="Run Depreciation", index=1).click()
    # The Run Depreciation submission screen is displayed with fields for asset book and period.
    page.element(css="h1,h2,h3", index=1).verify(V.like("*Run Depreciation*"))
