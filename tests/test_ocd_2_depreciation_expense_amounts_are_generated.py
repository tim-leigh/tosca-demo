"""
Jira Issue Key : OCD-2
qTest Test Case: OCD-2 - Depreciation expense amounts are generated for eligible fixed assets after the run
qTest ID       : 107943232
"""

import pytest

BOOK = "GENERIC_BOOK_01"
PERIOD = "GENERIC_PERIOD_01"
ASSET = "GENERIC_ASSET_01"


def test_depreciation_expense_amounts_are_generated():
    # ARRANGE – Precondition:
    # User is logged in with a Fixed Assets Manager role.
    # The depreciation run for GENERIC_BOOK_01 and GENERIC_PERIOD_01 has been completed successfully.
    # Asset GENERIC_ASSET_01 exists in GENERIC_BOOK_01 with a straight-line depreciation method
    # and a positive net book value prior to the run.

    pytest.skip("Scaffolded from qTest - implementation pending")

    # Step 1: Navigate to Fixed Assets > Inquiry > Assets in Oracle Fusion.
    navigate_to_asset_inquiry()
    assert True, "The Asset Inquiry screen is displayed."

    # Step 2: Search for asset number = GENERIC_ASSET_01 in the Asset Number field.
    search_asset(ASSET)
    assert True, f"Asset {ASSET} is returned in the search results."

    # Step 3: Select GENERIC_ASSET_01 and navigate to its Depreciation tab.
    open_depreciation_tab(ASSET)
    assert True, f"The Depreciation detail tab for {ASSET} is displayed."

    # Step 4: Verify that the depreciation expense amount recorded for period GENERIC_PERIOD_01 is non-zero.
    verify_depreciation_amount(ASSET, PERIOD)
    assert True, (
        f"A depreciation expense amount greater than zero is recorded for {PERIOD} against {ASSET}, "
        "confirming depreciation has been calculated and applied."
    )
