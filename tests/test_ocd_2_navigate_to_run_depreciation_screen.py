"""
Jira Issue Key : OCD-2
qTest Test Case: OCD-2 - User can navigate to the Run Depreciation screen in the Fixed Assets module
qTest ID       : 107945208
"""
import os
import pytest
from tbox_sdk import Secret, V


def test_navigate_to_run_depreciation_screen(tb) -> None:
    # Arrange — open application and sign in
    tb.open(os.environ["ORACLE_URL"])
    page = tb.web
    page.textbox(id="username").input(Secret.from_env("ORACLE_USER"))
    page.textbox(id="password").input(Secret.from_env("ORACLE_PASSWORD"))
    page.button(value="Sign In").click()

    # Precondition: User is logged in to Oracle Cloud Fusion with role = GENERIC_FA_ROLE_01.
    # The Fixed Assets module is accessible from the home page.
    # A valid asset book exists in the system.

    pytest.skip("Scaffolded from qTest - implementation pending")

    # Step 1: Navigate to the Oracle Cloud home page.
    # TODO: confirm with tx scan
    page.element(css="div.home-page").verify(V.like("*navigator*"))
    # Expected: The Oracle Cloud home page is displayed with the application navigator visible.

    # Step 2: Click the Fixed Assets application icon or link in the navigator.
    page.element(inner_text="Fixed Assets").click()
    # Expected: The Fixed Assets module home page is displayed.
    # TODO: confirm with tx scan
    page.element(css="div.fixed-assets-home").verify(V.like("*Fixed Assets*"))

    # Step 3: Click the Depreciation task link or menu item within Fixed Assets.
    page.element(inner_text="Depreciation").click()
    # Expected: The Depreciation task options are displayed, including an option to run depreciation.
    # TODO: confirm with tx scan
    page.element(css="div.depreciation-tasks").verify(V.like("*Run Depreciation*"))

    # Step 4: Click the Run Depreciation option.
    page.element(inner_text="Run Depreciation").click()
    # Expected: The Run Depreciation screen is displayed and ready for input.
    # TODO: confirm with tx scan
    page.element(css="div.run-depreciation-screen").verify(V.like("*Run Depreciation*"))
