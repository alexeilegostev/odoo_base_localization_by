from odoo import api, fields, models, _


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    @api.depends("quantity")
    def _compute_amounts(self):
        """Compute the amounts of the stock move"""
        for line_id in self:
            price = line_id.price_unit * (1 - (line_id.discount or 0.0) / 100.0)
            taxes = line_id.tax_id.compute_all(price, line_id.currency_id, line_id.quantity,
                                            product=line_id.product_id,
                                            partner=line_id.move_id.order_id.partner_shipping_id)
            line_id.update({
                "price_tax": sum(t.get("amount", 0.0) for t in taxes.get("taxes", [])),
                "price_total": taxes["total_included"],
                "price_subtotal": taxes["total_excluded"],
            })

    currency_id = fields.Many2one(comodel_name="res.currency", related="move_id.currency_id")
    price_unit = fields.Float(string="Unit Price", digits="Product Price", related="move_id.price_unit")
    tax_id = fields.Many2many(comodel_name="account.tax", string="Taxes", related="move_id.tax_id")
    discount = fields.Float(string="Discount (%)", digits="Discount", related="move_id.discount")
    price_subtotal = fields.Monetary(string="Subtotal", compute="_compute_amounts", store=True)
    price_tax = fields.Float(string="Total Tax", compute="_compute_amounts", store=True)
    price_total = fields.Monetary(string="Total", compute="_compute_amounts", store=True)
