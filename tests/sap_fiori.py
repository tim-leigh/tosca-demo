"""Page helpers for the SAP Fiori launchpad on sapdemo21 and the VA01 app.

Every control target lives in this file, so if a target is wrong you only
have to fix it here. The targets were NOT checked with `tx scan`: the system
could not be reached from the environment where this was written. Before the
first run, check them with:

    tx open "<launchpad url>"
    tx scan

and replace any target that does not match.

The launchpad login screen uses the standard SAP ids (USERNAME_FIELD-inner,
PASSWORD_FIELD-inner, LOGIN_LINK). "Create Sales Orders" (VA01) runs as
SAP GUI for HTML. Its ids are generated (for example M0:46::...), so its
fields are found by their `title` attribute (the field label) and not by id.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from datetime import date

# The Python import name of the `tbox-sdk` wheel is not stated in the SDK
# README. Adjust this one line if the wheel installs it under another name.
from tbox_sdk import Secret, V

LAUNCHPAD_URL = os.environ.get(
    "SAP_LAUNCHPAD_URL",
    "https://sapdemo21.tricentis.com:44301/sap/bc/ui5_ui5/ui2/ushell/shells/abap/FioriLaunchpad.html",
)
# Semantic object and action of the "Create Sales Orders" (VA01) tile.
CREATE_SALES_ORDER_HASH = os.environ.get("SAP_VA01_HASH", "#SalesOrder-create")

# Date format of the SAP user (SU3 > Defaults). The SAP default for US users is MM/DD/YYYY.
SAP_DATE_FORMAT = os.environ.get("SAP_DATE_FORMAT", "%m/%d/%Y")


def _env(name: str, default: str) -> str:
    return os.environ.get(name, default)


@dataclass(frozen=True)
class SalesOrderData:
    """Order data. Each value can be overridden with the environment variable named next to it.

    The defaults are the usual S/4HANA demo values (company code 1710). Change
    them if sapdemo21 uses other master data.
    """

    order_type: str = field(default_factory=lambda: _env("SO_ORDER_TYPE", "OR"))
    sales_org: str = field(default_factory=lambda: _env("SO_SALES_ORG", "1710"))
    distribution_channel: str = field(default_factory=lambda: _env("SO_DIST_CHANNEL", "10"))
    division: str = field(default_factory=lambda: _env("SO_DIVISION", "00"))
    sold_to: str = field(default_factory=lambda: _env("SO_SOLD_TO", "17100001"))
    material: str = field(default_factory=lambda: _env("SO_MATERIAL", "TG11"))
    quantity: str = field(default_factory=lambda: _env("SO_QUANTITY", "1"))
    # Today's date is used for the customer reference date and the requested delivery date.
    order_date: str = field(default_factory=lambda: date.today().strftime(SAP_DATE_FORMAT))

    @property
    def customer_reference(self) -> str:
        return f"TBOX-{self.order_date}"


def gui_field(page, label: str):
    """A SAP GUI for HTML input, found by its label (the input's `title` attribute)."""
    return page.textbox(css=f"input[title='{label}']")


def login(tb) -> None:
    """Sign in to the launchpad with SAP_USER and SAP_PASSWORD from the environment."""
    tb.open(LAUNCHPAD_URL)
    page = tb.web
    page.textbox(id="USERNAME_FIELD-inner").input(Secret.from_env("SAP_USER"))
    page.textbox(id="PASSWORD_FIELD-inner").input(Secret.from_env("SAP_PASSWORD"))
    page.button(id="LOGIN_LINK").click()
    # The launchpad shell header shows when the sign-in worked.
    page.element(id="shell-header").verify(V.like("*"))


def create_sales_order(tb, data: SalesOrderData) -> None:
    """Run VA01 from the launchpad: initial screen, header and item, save, check the message."""
    tb.open(LAUNCHPAD_URL + CREATE_SALES_ORDER_HASH)
    page = tb.web

    # Initial screen "Create Sales Documents".
    gui_field(page, "Sales Document Type").input(data.order_type)
    gui_field(page, "Sales Organization").input(data.sales_org)
    gui_field(page, "Distribution Channel").input(data.distribution_channel)
    gui_field(page, "Division").input(data.division)
    page.button(inner_text="Continue").click()

    # Overview screen: header.
    gui_field(page, "Sold-To Party").input(data.sold_to)
    gui_field(page, "Customer Reference").input(data.customer_reference)
    gui_field(page, "Customer Reference Date").input(data.order_date)
    gui_field(page, "Requested Delivery Date").input(data.order_date)

    # First item row. index=1 is the first row of the item table.
    page.textbox(css="input[title='Material']", index=1).input(data.material)
    page.textbox(css="input[title='Order Quantity']", index=1).input(data.quantity)

    page.button(inner_text="Save").click()

    # Success: the toast "Standard Order NNNN has been saved".
    page.element(css=".sapMMessageToast").verify(V.like("Standard Order * has been saved*"))
