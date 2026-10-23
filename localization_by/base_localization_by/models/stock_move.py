from odoo import models, fields, api, _

from odoo.tools import float_compare
from odoo.tools.misc import get_lang
from odoo.exceptions import UserError


class StockMove(models.Model):
    _inherit = "stock.move"

    @api.depends("quantity", "tax_id", "discount", "price_unit")
    def _compute_amounts(self):
        """Compute the amounts of the stock move"""
        for line_id in self:
            price = line_id.price_unit * (1 - (line_id.discount or 0.0) / 100.0)
            taxes = line_id.tax_id.compute_all(price, line_id.currency_id, line_id.quantity,
                                            product=line_id.product_id,
                                            partner=line_id.partner_id)
            line_id.update({
                "price_tax": sum(t.get("amount", 0.0) for t in taxes.get("taxes", [])),
                "price_total": taxes["total_included"],
                "price_subtotal": taxes["total_excluded"],
            })
        return

    @api.onchange("product_id")
    def _onchange_product_l10n(self):
        """Onchange product l10n"""
        if not self.product_id:
            return
        vals = {}
        if not self.product_uom or self.product_id.uom_id.id != self.product_uom.id:
            vals["product_uom"] = self.product_id.uom_id
            vals["product_uom_qty"] = self.product_uom_qty or 1

        product_id = self.product_id.with_context(
            lang=get_lang(self.env, self.picking_id.partner_id.lang).code,
            partner=self.picking_id.partner_id,
            quantity=vals.get("product_uom_qty") or self.product_uom_qty if self.product_uom_qty else 1,
            date=self.date,
            pricelist=self.picking_id.pricelist_id.id,
            uom=self.product_uom.id
        )
        vals.update({"name": product_id.get_product_multiline_description_sale()})
        self._compute_tax_id()
        if self.picking_id.pricelist_id and self.picking_id.partner_id:
            vals["price_unit"] = self.env["account.tax"]._fix_tax_included_price_company(
                self._get_display_price(product_id), product_id.taxes_id, self.tax_id, self.company_id)
        self.update(vals)

    @api.onchange("product_uom", "product_uom_qty")
    def product_uom_change(self):
        """Product oum change"""
        if not self.product_uom or not self.product_id:
            self.price_unit = 0.0
            return
        if self.picking_id.pricelist_id and self.picking_id.partner_id:
            product_id = self.product_id.with_context(
                lang=self.order_id.partner_id.lang,
                partner=self.picking_id.partner_id,
                quantity=self.product_uom_qty or 1,
                date=self.picking_id.date,
                pricelist=self.picking_id.pricelist_id.id,
                uom=self.product_uom.id,
                fiscal_position=self.env.context.get("fiscal_position")
            )
            self.price_unit = self.env["account.tax"]._fix_tax_included_price_company(
                self._get_display_price(product_id), product_id.taxes_id, self.tax_id, self.company_id)

    def _compute_tax_id(self):
        for line_id in self:
            fpos = line_id.picking_id.fiscal_position_id or line_id.picking_id.partner_id.property_account_position_id
            # If company_id is set, always filter taxes by the company
            taxes = line_id.product_id.taxes_id.filtered(lambda r: not line_id.company_id or r.company_id == line_id.company_id)
            line_id.tax_id = fpos.map_tax(taxes, line_id.product_id, line_id.picking_id.partner_id) if fpos else taxes

    @api.depends("product_id", "quantity")
    def _compute_weight(self):
        """Compute weight"""
        for line_id in self:
            if line_id.product_id and line_id.quantity:
                line_id.weight = line_id.product_id.weight * line_id.quantity
            else:
                line_id.weight = 0

    @api.depends("product_id", "quantity")
    def _compute_volume(self):
        """Compute volume"""
        for line_id in self:
            if line_id.product_id and line_id.quantity:
                line_id.volume = line_id.product_id.volume * line_id.quantity
            else:
                line_id.volume = 0

    order_id = fields.Many2one(comodel_name="sale.order", string="Order Reference")
    order_line_id = fields.Many2one(comodel_name="sale.order.line", string="Order line")
    currency_id = fields.Many2one(comodel_name="res.currency")
    price_unit = fields.Float(string="Unit Price", digits="Product Price", default=0.0, readonly=False, store=True)
    tax_id = fields.Many2many(comodel_name="account.tax", string="Taxes", readonly=False, store=True)
    discount = fields.Float(string="Discount (%)", digits="Discount", default=0.0, readonly=False, store=True)
    price_subtotal = fields.Monetary(string="Subtotal", readonly=True, compute="_compute_amounts", store=True)
    price_tax = fields.Float(string="Total Tax", readonly=True, compute="_compute_amounts", store=True)
    price_total = fields.Monetary(string="Total", readonly=True, compute="_compute_amounts", store=True)
    cost = fields.Monetary(string="Cost")
    weight = fields.Float(string="Weight", compute="_compute_weight", store=True)
    volume = fields.Float(string="Volume", compute="_compute_volume", store=True)
    cargo_places = fields.Float(string="Cargo places", default=1.0)
    note = fields.Char(string="Note")
    pricelist_id = fields.Many2one(comodel_name="product.pricelist", string="pricelist")
    payment_term_id = fields.Many2one(comodel_name="account.payment.term", string="Payment Terms",
                                      domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    fiscal_position_id = fields.Many2one(comodel_name="account.fiscal.position", string="Fiscal Position",
                                         domain="[('company_id', '=', company_id)]", check_company=True,
                                         help="Fiscal positions are used to adapt taxes and accounts for particular"
                                              "customers.The default value comes from the customer.")

    def _get_new_picking_values(self):
        """Method for getting new picking values"""
        vals = super(StockMove, self)._get_new_picking_values()
        vals.update({
            "pricelist_id": self.mapped("pricelist_id").id,
            "currency_id": self.mapped("currency_id").id,
            "sale_order_id": self.mapped("order_id").id if len(self.mapped("order_id")) == 1 else False,
            "payment_term_id": self.mapped("payment_term_id").id if len(self.mapped("payment_term_id")) == 1 else False,
            "fiscal_position_id": self.mapped("fiscal_position_id").id if len(
                self.mapped("fiscal_position_id")) == 1 else False,
        })
        return vals

    def _get_display_price(self, product_id):
        """Display price"""
        if self.picking_id.pricelist_id.discount_policy == "with_discount":
            return product_id.with_context(pricelist=self.picking_id.pricelist_id.id).standard_price
        product_context = dict(self.env.context, partner_id=self.picking_id.partner_id.id,
                               date=self.picking_id.date_order, uom=self.product_uom.id)

        final_price, rule_id = self.picking_id.pricelist_id.with_context(product_context).get_product_price_rule(
            self.product_id, self.quantity or 1.0, self.picking_id.partner_id)
        base_price, currency = self.with_context(product_context)._get_real_price_currency(product_id, rule_id,
                                                                                           self.quantity,
                                                                                           self.product_uom,
                                                                                           self.picking_id.pricelist_id.id)
        if currency != self.picking_id.pricelist_id.currency_id:
            base_price = currency._convert(
                base_price, self.picking_id.pricelist_id.currency_id,
                self.picking_id.company_id or self.env.company, self.picking_id.date or fields.Date.today())
        return max(base_price, final_price)
