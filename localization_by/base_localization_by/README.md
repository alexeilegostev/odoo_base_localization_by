# base_localization_by — Belarus - Accounting

Odoo 17 localization for Belarus: statutory chart of accounts, VAT (0/10/20/25%), and printable documents (TN, TTN, CMR, acts).

Technical name: `base_localization_by` · Version: `17.0.2` · License: LGPL-3 · Country: `by`

---

## Purpose

Provides a starting accounting setup for companies in Belarus:

1. **Belarus statutory chart of accounts** (chart template `by`)
2. **VAT** at the main rates (sale / purchase)
3. **Printable documents** for sales and deliveries (TN, TTN, acts, CMR, etc.)
4. **Fields and attributes** for transport and accounting documents (partner, company, warehouse, delivery)

After installation, select **Belarus - Accounting** to load accounts, taxes, and company defaults.

---

## Chart of accounts

Based on the **Belarus statutory chart of accounts** (~64 accounts).

Main synthetic accounts:

| Code | Purpose |
|------|---------|
| 01, 02, 04, 05, 07, 08 | Long-term assets and depreciation |
| 10, 15, 16, 18, 20, 23, 25, 26, 28 | Inventories, production, recoverable VAT |
| 41–45 | Goods, finished products, shipments |
| 50–58 | Cash and short-term investments |
| 60, 62, 66–71, 76 | Settlements (suppliers, customers, taxes, payroll) |
| 80–86 | Equity and targeted financing |
| 90xx, 91xx, 94–99 | Income, expenses, profit and loss |

Working sub-accounts added for Odoo:

- `6002` / `6202` — advances paid / received  
- `6203` — PoS receivables  
- `681`–`683` — VAT and other tax settlements  
- `9001`–`9005` — revenue, COGS, administrative and selling expenses  
- `9101` / `9102` — other income and expenses  

Template defaults:

- receivable → `62`, payable → `60`  
- income → `9001`, category expense → `9003`  
- stock valuation → `41`, input/output → `15` / `45`  
- bank / cash / transfers → prefixes `51` / `50` / `57`

---

## Taxes (VAT)

Sale and purchase rates: **0%, 10%, 20%, 25%**.

- Output VAT → account `681`  
- Input VAT → account `18`  

Advance products are created by the template and linked to `6202` / `6002`.

---

## Printable documents

Available from **invoice (`account.move`)** and/or **picking (`stock.picking`)**:

- Certificate of completion (act of performed works)  
- Account protocol  
- Specification  
- **TN** / **TTN** (vertical, horizontal, with attachment)  
- **CMR**  

Report access is controlled by security groups (separate groups per document type).

Amount-in-words and name inflection use the Python packages `pytils` and `petrovich`.

---

## Functional extensions

- **Stock / delivery:** prices, taxes, discounts on `stock.move` / `stock.picking`; TTN fields (driver, vehicle, loading/unloading, power of attorney, weight, cargo places, etc.)
- **Partner / company:** OKPO, registry info; driver and “leave allowed” flags; driver license series/number
- **Transport:** integration with `res.transport` (`ru_transport`)
- **Sales:** transfer of prices/taxes/fiscal position from the order into procurement/picking

---

## Dependencies

**Odoo:** `account`, `sale`, `stock`, `delivery`, `product`, `uom`, `sale_project`, `stock_landed_costs`, `contracts`, `account_fleet`, `ru_transport`

**Python:** `pytils`, `petrovich`

---

## Installation

1. Add the module directory to `addons_path` (folder name must be `base_localization_by`).
2. Install Python dependencies: `pytils`, `petrovich`.
3. Update the Apps list and install **Belarus - Accounting**.
4. When creating or configuring a company, apply the Belarus localization (chart template `by`).

Prefer installing on a clean database or a new company.

---

## Limitations

- This is a **base** localization: chart of accounts + VAT + printable documents.  
- No e-invoicing (ESChF), VAT return, purchase/sales books, or full tax-authority reporting.  
- Account `90` is split into Odoo sub-accounts `9001`–`9005` (income/expense types), because Odoo has no single matching account like classic account 90 postings.  
- Depends on `ru_transport` and `contracts`.

---

## Author

iCode — https://icode.by
