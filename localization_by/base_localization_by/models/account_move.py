from collections import defaultdict

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.tools import formatLang


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.depends("line_ids.price_subtotal", "line_ids.tax_base_amount", "line_ids.tax_line_id", "partner_id",
                 "currency_id")
    def _compute_invoice_taxes_by_group(self):
        """Compute invoice taxes by group"""
        for move_id in self:

            # Not working on something else than invoices.
            if not move_id.is_invoice(include_receipts=True):
                move_id.amount_by_group = []
                continue

            lang_env = move_id.with_context(lang=move_id.partner_id.lang).env
            balance_multiplicator = -1 if move_id.is_inbound() else 1

            tax_line_ids = move_id.line_ids.filtered("tax_line_id")
            base_lines_ids = move_id.line_ids.filtered("tax_ids")

            tax_group_mapping = defaultdict(lambda: {
                "base_lines": set(),
                "base_amount": 0.0,
                "tax_amount": 0.0,
            })

            # Compute base amounts.
            for base_line_id in base_lines_ids:
                base_amount = balance_multiplicator * (
                    base_line_id.amount_currency if base_line_id.currency_id else base_line_id.balance)

                for tax in base_line_id.tax_ids.flatten_taxes_hierarchy():

                    if base_line_id.tax_line_id.tax_group_id == tax.tax_group_id:
                        continue

                    tax_group_vals = tax_group_mapping[tax.tax_group_id]
                    if base_line_id not in tax_group_vals["base_lines"]:
                        tax_group_vals["base_amount"] += base_amount
                        tax_group_vals["base_lines"].add(base_line_id)

            # Compute tax amounts.
            for tax_line_id in tax_line_ids:
                tax_amount = balance_multiplicator * (
                    tax_line_id.amount_currency if tax_line_id.currency_id else tax_line_id.balance)
                tax_group_vals = tax_group_mapping[tax_line_id.tax_line_id.tax_group_id]
                tax_group_vals["tax_amount"] += tax_amount

            tax_group_ids = sorted(tax_group_mapping.keys(), key=lambda x: x.sequence)
            amount_by_group = []
            for tax_group_id in tax_group_ids:
                tax_group_vals = tax_group_mapping[tax_group_id]
                amount_by_group.append((
                    tax_group_id.name,
                    tax_group_vals["tax_amount"],
                    tax_group_vals["base_amount"],
                    formatLang(lang_env, tax_group_vals["tax_amount"], currency_obj=move_id.currency_id),
                    formatLang(lang_env, tax_group_vals["base_amount"], currency_obj=move_id.currency_id),
                    len(tax_group_mapping),
                    tax_group_id.id
                ))
            move_id.amount_by_group = amount_by_group

    @api.depends("invoice_line_ids.weight")
    def _compute_weight_total(self):
        """Compute total weight"""
        for record_id in self:
            record_id.weight_total = sum(record_id.invoice_line_ids.mapped("weight"))

    @api.depends("invoice_line_ids.cargo_places")
    def _compute_cargo_places_total(self):
        """Compute total cargo places"""
        for record_id in self:
            record_id.cargo_places_amount = sum(
                record_id.invoice_line_ids.filtered(
                    lambda l: l.display_type not in ["line_note", "line_section"]).mapped("cargo_places"))

    @api.onchange("driver_employee_id")
    def _onchange_driver_employee_id(self):
        """Onchange driver employee"""
        if self.driver_employee_id:
            self.driver_other = False

    @api.onchange("driver_other")
    def _onchange_driver_other(self):
        """Onchange other driver"""
        if self.driver_other:
            self.driver_employee_id = False

    @api.onchange("loading_start", "loading_end")
    def _onchange_loading_dates(self):
        """Onchange loading dates"""
        self.check_date_interval(self.loading_start, self.loading_end)

    @api.onchange("unloading_start", "unloading_end")
    def _onchange_unloading_dates(self):
        """Onchange unloading dates"""
        self.check_date_interval(self.unloading_start, self.unloading_end)

    # fields for report data
    customer_automotive_carriage_id = fields.Many2one(comodel_name="res.partner",
                                                      string="Customer of road transportation")
    vehicle = fields.Char(string="Vehicle")
    trailer = fields.Char(string="Trailer")
    driver_other = fields.Char(string="Driver other")
    driver_employee_id = fields.Many2one(comodel_name="res.partner", string="Driver employee")
    waybill = fields.Char(string="Waybill")
    basis_document = fields.Char(string="Basis document")
    loading_id = fields.Many2one(comodel_name="res.partner", string="Loading point")
    unloading_id = fields.Many2one(comodel_name="res.partner", string="Unloading point")
    leave_allowed_by_id = fields.Many2one(comodel_name="res.partner", string="Leave allowed by")
    seal = fields.Char(string="Seal")
    attorney_number = fields.Char(string="Number", required=False)
    attorney_date = fields.Date(string="Date", required=False)
    attorney_company = fields.Many2one(comodel_name="res.partner", required=False, store=True)
    cargo_accepted_for_transportation_by = fields.Char(string="Cargo accepted for transportation by")
    cargo_released_by = fields.Many2one(comodel_name="res.partner")
    cargo_accepted_by = fields.Char(string="Cargo accepted by")
    loading_start = fields.Datetime(string="Loading")
    loading_end = fields.Datetime(string="Loading end")
    loading_contractor = fields.Char(string="Loading contractor")
    loading_method = fields.Selection(selection=[("manual", "Manual"), ("mechanical", "Mechanical")],
                                      string="Loading method")
    unloading_start = fields.Datetime(string="Unloading")
    unloading_end = fields.Datetime(string="Unloading end")
    unloading_contractor = fields.Char(string="Unloading contractor")
    unloading_method = fields.Selection(selection=[("manual", "Manual"), ("mechanical", "Mechanical")],
                                        string="Unloading method")
    consignment_note = fields.Char(string="Consignment number")
    consignment_date = fields.Date(string="Consignment date")
    weight_total = fields.Float(string="Weight total", compute="_compute_weight_total")
    cargo_places_amount = fields.Float(string="Amount of cargo places total", readonly=True,
                                       compute="_compute_cargo_places_total")
    amount_by_group = fields.Binary(string="Tax amount by group", compute="_compute_invoice_taxes_by_group")
    related_delivery_id = fields.Many2one(comodel_name="stock.picking", string="Related Delivery")

    @staticmethod
    def check_date_interval(date_start=False, date_end=False):
        """Check date interval and validate them"""
        if date_start and date_end and date_start > date_end:
            raise UserError(_("End date shouldn't be less then start date."))


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    @api.depends("price_subtotal", "price_total")
    def _compute_price_tax(self):
        """Compute price tax"""
        for line_id in self:
            line_id.price_tax = line_id.price_total - line_id.price_subtotal

    @api.depends("product_id", "quantity")
    def _compute_weight(self):
        """Compute weight"""
        for line_id in self:
            line_id.weight = line_id.product_id.weight * line_id.quantity

    price_tax = fields.Float(string="Total Tax", compute="_compute_price_tax", store=True)
    weight = fields.Float(string="Weight", compute="_compute_weight", store=True)
    cargo_places = fields.Float(string="Cargo places", default=1.0)
    note = fields.Char(string="Note", required=False)

    def get_price_unit_in_company_currency(self):
        """Returns the price unit in the company currency"""
        if self.env.company.currency_id == self.currency_id:
            return self.price_unit
        date = self.move_id.invoice_date or fields.Date.today()
        return self.currency_id._convert(
            from_amount=self.price_unit,
            to_currency=self.env.company.currency_id,
            company=self.env.company,
            date=date,
        )
