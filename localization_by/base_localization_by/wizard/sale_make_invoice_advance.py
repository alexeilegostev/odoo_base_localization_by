# -*- coding: utf-8 -*-

from odoo import models


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    def _prepare_down_payment_product_values(self):
        self.ensure_one()
        result = super()._prepare_down_payment_product_values()
        if self.env.company.chart_template in ("generic_coa", "ru", "by"):
            account_id = self.env["account.account"].search([("account_type", "=", "asset_prepayments"), ("company_id", "=", self.env.company.id)], limit=1)
            if account_id:
                result.update({
                    "property_account_income_id": account_id.id,
                    "property_account_expense_id": account_id.id,
                })
        return result
