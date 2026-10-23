from odoo import api, models, _


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _prepare_procurement_values(self, group_id=False):
        """Add custom keys that could be used in move/po creation"""
        values = super(SaleOrderLine, self)._prepare_procurement_values(group_id)
        values.update({
            "price_unit": self.price_unit,
            "tax_id": [(6, 0, self.tax_id.ids)],
            "discount": self.discount,
            "order_id": self.order_id.id,
            "order_line_id": self.id,
            "currency_id": self.currency_id.id,
            "pricelist_id": self.order_id.pricelist_id.id,
            "payment_term_id": self.order_id.payment_term_id.id,
            "fiscal_position_id": self.order_id.fiscal_position_id.id,
        })
        return values
