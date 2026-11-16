# tosca-demo

A TBox SDK (0.4.136) Python test that creates a standard sales order with
**Create Sales Orders (VA01)** from the SAP Fiori launchpad on sapdemo21, and
passes when the toast "Standard Order NNNN has been saved" appears.

## Setup

```bash
python -m venv .venv-tx
source .venv-tx/bin/activate            # Windows PowerShell: .venv-tx\Scripts\Activate.ps1
pip install <bundle>/python/tbox_sdk-0.4.136-py3-none-<wheel tag>.whl
pip install -r requirements.txt
```

## Credentials

The test reads `SAP_USER` and `SAP_PASSWORD` from the environment. Never put
them in the repo.

## Run

```bash
pytest
```

Use `TBOX_HEADLESS=0` for a visible browser. Run one test at a time.

## Order data

The defaults are S/4HANA demo values. Override any of them with these environment variables:

| Variable | Default | Field |
|---|---|---|
| `SO_ORDER_TYPE` | `OR` | Sales Document Type |
| `SO_SALES_ORG` | `1710` | Sales Organization |
| `SO_DIST_CHANNEL` | `10` | Distribution Channel |
| `SO_DIVISION` | `00` | Division |
| `SO_SOLD_TO` | `17100001` | Sold-To Party |
| `SO_MATERIAL` | `TG11` | Material |
| `SO_QUANTITY` | `1` | Order Quantity |
| `SAP_DATE_FORMAT` | `%m/%d/%Y` | Format of today's date (set it to match the SAP user's date format) |

Today's date is used as the customer reference date and the requested
delivery date, and the customer reference is `TBOX-<date>`.

## Not yet verified

The control targets in `tests/sap_fiori.py` have not been checked against
the live system. Run `tx open <launchpad url>` and `tx scan` and fix the
targets there before the first real run.
