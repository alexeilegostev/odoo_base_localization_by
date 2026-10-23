# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class StockRule(models.Model):
    _inherit = "stock.rule"

    def _get_custom_move_fields(self):
        """Override the method in order to add fields from procurement 'values' argument to move data"""
        fields = super(StockRule, self)._get_custom_move_fields()
        fields.extend([
            "contract_number",
            "contract_date",
            "currency_id",
            "discount",
            "order_line_id",
            "order_id",
            "price_unit",
            "pricelist_id",
            "tax_id",
            "payment_term_id",
            "fiscal_position_id",
        ])
        return fields
