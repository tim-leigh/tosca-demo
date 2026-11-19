"""
Jira issue: OCD-2
qTest test case: OCD-2 - User can navigate to the Fixed Assets module and open the depreciation submission screen
qTest ID: 107947360
"""
import os
import pytest
from tbox_sdk import Secret, V


def test_navigate_to_fixed_assets_depreciation_screen(tb) -> None:
    # Precondition: User GENERIC_FA_USER_01 is logged in to Oracle Fusion with the Fixed Assets Manager role.
    # The Oracle Fusion environment is accessible and responsive.

    # Arrange: open Oracle Fusion and sign in
    tb.open(os.environ["ORACLE_URL"])
    page = tb.web
    page.textbox(id="username").input(Secret.from_env("ORACLE_USER"))
    page.textbox(id="password").input(Secret.from_env("ORACLE_PASSWORD"))
    page.button(value="Sign In").click()

    # Step 1: Navigate to the Oracle Fusion home page as GENERIC_FA_USER_01.
    # (Sign-in above lands on the home page.)
    # The Oracle Fusion home page loads and displays the application Navigator or home icons for the user's assigned roles.
    page.element(css="div.home-page").verify(V.like("*Navigator*"))

    # Step 2: Click the Navigator menu icon on the Oracle Fusion home page.
    page.element(css="button.navigator-menu-icon").click()
    # The Navigator panel expands and displays a list of available application modules.
    page.element(css="div.navigator-panel").verify(V.like("*Fixed Assets*"))

    # Step 3: Select Fixed Assets from the Navigator module list.
    page.element(inner_text="Fixed Assets").click()
    # The Fixed Assets module landing page opens without errors.
    page.element(css="div.module-landing-page").verify(V.like("*Fixed Assets*"))

    # Step 4: Click the Depreciation menu option or task link within the Fixed Assets module.
    page.element(inner_text="Depreciation").click()
    # The depreciation submission screen opens and displays the required fields for initiating a depreciation run (e.g., asset book, period).
    page.element(css="div.depreciation-submission-screen").verify(V.like("*Asset Book*"))
