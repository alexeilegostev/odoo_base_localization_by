# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo
#    Copyright (C) 2024 iCode (<https://icode.by>).
#
##############################################################################

{
    "name": "Belarus - Accounting",
    "version": "17.0.2",
    "category": "Accounting/Localizations/Account Charts",
    "description":
        """
Belarus localization base module for Odoo 17+.

Includes the statutory chart of accounts of the Republic of Belarus,
VAT taxes, and printable documents (TN, TTN, CMR, etc.).
        """,
    "author": "iCode",
    "countries": ["by"],
    "website": "http://icode.by",
    "depends": [
        "account",
        "uom",
        "product",
        "sale_project",
        "sale",
        "stock",
        "stock_landed_costs",
        "delivery",
        "contracts",
        "ru_transport",
        "account_fleet",
    ],
    "external_dependencies": {
        "python": ["pytils", "petrovich"],
    },
    "data": [
        "data/account_account_data.xml",
        "data/papers_format.xml",
        "security/security.xml",
        "security/ir.model.access.csv",
        "report/report.xml",
        "report/acceptance_report.xml",
        "report/account_protocol_inv.xml",
        "report/account_protocol_pick.xml",
        "report/specification_inv.xml",
        "report/specification_pick.xml",
        "report/report_tn_inv.xml",
        "report/report_ttn_inv.xml",
        "report/report_tn_with_attach_inv.xml",
        "report/report_ttn_with_attach_inv.xml",
        "report/report_tn_pick.xml",
        "report/report_ttn_pick.xml",
        "report/report_tn_with_attach_pick.xml",
        "report/report_ttn_with_attach_pick.xml",
        "report/report_cmr_by.xml",
        "views/account_move_views.xml",
        "views/res_partner.xml",
        "views/res_company_views.xml",
        "views/stock_move_line_views.xml",
        "views/stock_picking_views.xml",
        "views/res_transport.xml",
    ],
    "demo": [
        "demo/demo_company.xml",
    ],
    "license": "LGPL-3",
}
