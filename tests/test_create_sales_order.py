"""Create a standard sales order with VA01 from the SAP Fiori launchpad.

Needs SAP_USER and SAP_PASSWORD in the environment. The order data and the
targets are in sap_fiori.py.
"""

from sap_fiori import SalesOrderData, create_sales_order, login


def test_create_sales_order(tb) -> None:
    login(tb)
    create_sales_order(tb, SalesOrderData())
