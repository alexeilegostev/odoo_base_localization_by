from functools import partial

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools.misc import formatLang


class Picking(models.Model):
    _inherit = "stock.picking"

    @api.depends("move_ids_without_package.price_total")
    def _amount_all_(self):
        """Compute the total amounts of the picking"""
        for pick_id in self:
            amount_untaxed = amount_tax = 0.0
            for move_line_id in pick_id.move_ids_without_package:
                amount_untaxed += move_line_id.price_subtotal
                amount_tax += move_line_id.price_tax
            pick_id.update({
                "amount_untaxed": amount_untaxed,
                "amount_tax": amount_tax,
                "amount_total": amount_untaxed + amount_tax,
            })

    def _set_customer_automotive_carriage_id(self):
        """Pass"""
        pass

    def _set_basis_document(self):
        """Pass"""
        pass

    def _set_loading_id(self):
        """Pass"""
        pass

    def _set_unloading_id(self):
        """Pass"""
        pass

    def _set_leave_allowed_by_id(self):
        """Pass"""
        pass

    def _set_cargo_released_by_id(self):
        """Pass"""
        pass

    @api.onchange("vehicle_id")
    def _onchange_license_plate(self):
        """Set lincense when vehicle"""
        self.license_plate = self.vehicle_id.license_plate
        if self.vehicle_id.driver_employee_id:
            self.driver_employee_id = self.vehicle_id.driver_employee_id

    @api.onchange("trailer_id")
    def _onchange_trailer_id(self):
        """Set lincense when trailer"""
        self.trailer_license_plate = self.trailer_id.license_plate
        if self.trailer_id.driver_employee_id:
            self.driver_employee_id = self.trailer_id.driver_employee_id

    @api.depends("partner_id")
    def _compute_basic_document(self):
        """Compute basic document"""
        for record_id in self:
            if ("sale_id" in record_id._fields) and record_id.sale_id and record_id.sale_id.contract_id:
                record_id.basis_document = _("{name} at {date}").format(
                    name=record_id.sale_id.contract_id.name,
                    date=record_id.sale_id.contract_date,
                )
            elif ("purchase_id" in self._fields) and record_id.purchase_id and record_id.purchase_id.contract_id:
                record_id.basis_document = _("{name} at {date}").format(
                    name=record_id.sale_id.contract_id.name,
                    date=record_id.sale_id.contract_date,
                )

    @api.depends("partner_id")
    def _compute_customer_automotive_carriage_id(self):
        """Compute parametrs for report info when set partner"""
        for record_id in self:
            record_id.customer_automotive_carriage_id = record_id.partner_id
            record_id.loading_id = record_id.company_id.partner_id
            record_id.unloading_id = record_id.partner_id
            if record_id.partner_id and record_id.partner_id.is_leave_allowed:
                record_id.leave_allowed_by_id = record_id.partner_id
                record_id.cargo_released_by_id = record_id.partner_id

    @api.depends("move_ids_without_package.weight")
    def _compute_weight_total(self):
        """Compute total weight"""
        for record_id in self:
            record_id.weight_total = sum(record_id.move_ids_without_package.mapped("weight"))

    @api.depends("move_ids_without_package.volume")
    def _compute_volume_total(self):
        """Compute total volume"""
        for record_id in self:
            record_id.volume_total = sum(record_id.move_ids_without_package.mapped("volume"))

    @api.depends("move_ids_without_package.cargo_places")
    def _compute_amount_cargo_places(self):
        """Compute amount cargo places"""
        for record_id in self:
            record_id.amount_cargo_places = sum(record_id.move_ids_without_package.mapped("cargo_places"))

    @api.onchange("driver_employee_id")
    def _onchange_driver_employee_id(self):
        """Onchange driver employee"""
        if self.driver_employee_id:
            self.driver_other_id = False
            self.cargo_accepted_by_id = self.driver_employee_id
            self.cargo_accepted_for_transportation_by_id = self.driver_employee_id

    @api.onchange("driver_other_id")
    def _onchange_driver_other(self):
        """Onchange other driver"""
        if self.driver_other_id:
            self.driver_employee_id = False

    @api.onchange("partner_id")
    def _onchange_partner_id(self):
        """Set pricelist for customer"""
        if not self.partner_id:
            return
        self.pricelist_id = self.partner_id.property_product_pricelist.id if self.partner_id.property_product_pricelist else False
        self.fiscal_position_id = self.partner_id.property_account_position_id.id if self.partner_id.property_account_position_id else False

    @staticmethod
    def check_date_interval(date_start=False, date_end=False):
        """Check date interval and validate them"""
        if date_start and date_end and date_start > date_end:
            raise UserError(_("End date shouldn't be less then start date."))

    @api.onchange("loading_start", "loading_end")
    def _onchange_loading_dates(self):
        """Onchange loading dates"""
        self.check_date_interval(self.loading_start, self.loading_end)

    @api.onchange("unloading_start", "unloading_end")
    def _onchange_unloading_dates(self):
        """Onchange unloading dates"""
        self.check_date_interval(self.unloading_start, self.unloading_end)

    currency_id = fields.Many2one(comodel_name="res.currency", related="pricelist_id.currency_id", string="Currency")
    pricelist_id = fields.Many2one(comodel_name="product.pricelist", string="Pricelist", check_company=True,
                                   domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    amount_untaxed = fields.Monetary(string="Untaxed Amount", store=True, readonly=True, compute="_amount_all_",
                                     tracking=5)
    amount_by_group = fields.Binary(string="Tax amount by group", compute="_amount_by_group")
    amount_tax = fields.Monetary(string="Taxes", store=True, compute="_amount_all_", readonly=True)
    amount_total = fields.Monetary(string="Total", store=True, readonly=True, compute="_amount_all_", tracking=4)
    sale_order_id = fields.Many2one(comodel_name="sale.order", string="Sale Order")
    fiscal_position_id = fields.Many2one(comodel_name="account.fiscal.position", string="Fiscal Position",
                                         domain="[('company_id', '=', company_id)]", check_company=True,
                                         help="Fiscal positions are used to adapt taxes and accounts for particular"
                                              "customers.The default value comes from the customer.")
    payment_term_id = fields.Many2one(comodel_name="account.payment.term", string="Payment Terms",
                                      domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    invoice_partner_bank_id = fields.Many2one(comodel_name="res.partner.bank", string="Bank Account",
                                              help="Bank Account Number to which the invoice will be paid.",
                                              domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    # fields for reports
    customer_automotive_carriage_id = fields.Many2one(
        comodel_name="res.partner",
        string="Customer of road transportation",
        compute="_compute_customer_automotive_carriage_id",
        store=True,
        inverse="_set_customer_automotive_carriage_id",
    )
    vehicle_id = fields.Many2one(comodel_name="res.transport", string="Vehicle")
    trailer_id = fields.Many2one(
        comodel_name="res.transport",
        string="Trailer",
        domain="[('transport_type', '=', 'trailer')]",
    )
    driver_other_id = fields.Many2one(
        comodel_name="res.partner",
        string="Driver other",
        domain="[('is_driver', '=', True)]")
    driver_employee_id = fields.Many2one(
        comodel_name="res.partner",
        string="Driver employee",
        domain="[('is_driver', '=', True)]",
    )
    waybill = fields.Char(string="Waybill")
    basis_document = fields.Char(
        string="Basis document",
        compute="_compute_basic_document",
        store=True,
        inverse="_set_basis_document",
    )
    loading_id = fields.Many2one(
        comodel_name="res.partner",
        string="Loading point",
        compute="_compute_customer_automotive_carriage_id",
        store=True,
        inverse="_set_loading_id"
    )
    unloading_id = fields.Many2one(
        comodel_name="res.partner",
        string="Unloading point",
        compute="_compute_customer_automotive_carriage_id",
        store=True,
        inverse="_set_unloading_id"
    )
    leave_allowed_by_id = fields.Many2one(
        comodel_name="res.partner",
        string="Leave allowed by",
        domain="[('is_leave_allowed', '=', True)]",
        compute="_compute_customer_automotive_carriage_id",
        store=True,
        inverse="_set_leave_allowed_by_id"
    )
    seal = fields.Char(string="Seal")
    attorney_number = fields.Char(string="Number", required=False)
    attorney_date = fields.Date(string="Date", required=False)
    attorney_company = fields.Many2one(comodel_name="res.partner", required=False, store=True)
    cargo_accepted_for_transportation_by_id = fields.Many2one(
        comodel_name="res.partner",
        string="Cargo accepted by transportation",
        domain="[('is_leave_allowed', '=', True)]",
    )
    cargo_released_by_id = fields.Many2one(
        comodel_name="res.partner",
        string="Cargo Release by",
        domain="[('is_leave_allowed', '=', True)]",
        compute="_compute_customer_automotive_carriage_id",
        store=True,
        inverse="_set_cargo_released_by_id",
    )
    cargo_accepted_by_id = fields.Many2one(
        comodel_name="res.partner",
        string="Cargo accepted by",
        domain="[('is_leave_allowed', '=', True)]",
    )
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
    weight_total = fields.Float(string="Weight total", readonly=True, compute="_compute_weight_total", store=True)
    volume_total = fields.Float(string="Volume total", readonly=True, compute="_compute_volume_total", store=True)
    amount_cargo_places = fields.Float(string="Amount cargo places", readonly=True,
                                       compute="_compute_amount_cargo_places", store=True)
    license_plate = fields.Char(string="License plate")
    trailer_license_plate = fields.Char(string="Trailer license ")
    packaging = fields.Char(string="Packaging (if available)")
    gross_weight_actual = fields.Float(string="Gross cargo weight, kg (actual)")
    cargo_volume = fields.Float(string="Cargo volume in cubic meters")
    cargo_declared_value = fields.Float(string="Declared value of the cargo")
    transfer_with_the_goods = fields.Char(string="Documents were transferred with the goods")

    def _amount_by_group(self):
        """Compute amounts of taxes by group in the picking"""
        for picking_id in self:
            currency = picking_id.currency_id or picking_id.company_id.currency_id
            fmt = partial(formatLang, self.with_context(lang=picking_id.partner_id.lang).env, currency_obj=currency)
            res = {}
            for line_id in picking_id.move_ids_without_package:
                price_reduce = line_id.price_unit * (1.0 - line_id.discount / 100.0)
                tax_ids = line_id.tax_id.compute_all(price_reduce, quantity=line_id.quantity,
                                                   product=line_id.product_id, partner=picking_id.partner_id)["taxes"]
                for tax_id in line_id.tax_id:
                    group = tax_id.tax_group_id
                    res.setdefault(group, {"amount": 0.0, "base": 0.0})
                    for t in tax_ids:
                        if t["id"] == tax_id.id or t["id"] in tax_id.children_tax_ids.ids:
                            res[group]["amount"] += t["amount"]
                            res[group]["base"] += t["base"]
            res = sorted(res.items(), key=lambda l: l[0].sequence)
            picking_id.amount_by_group = [(
                l[0].name, l[1]["amount"], l[1]["base"],
                fmt(l[1]["amount"]), fmt(l[1]["base"]),
                len(res),
            ) for l in res]
