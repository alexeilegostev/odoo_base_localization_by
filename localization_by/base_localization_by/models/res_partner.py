from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    kpp = fields.Char(string="KPP")
    ogrn = fields.Char(string="OGRN")
    ogrnip = fields.Char(string="OGRNIP")
    okpo = fields.Char(string="OKPO")
    okato = fields.Char(string="OKATO")
    registry_info = fields.Char(string="Registry info")
    is_driver = fields.Boolean(string="Is Driver")
    driver_license_series = fields.Char(string="Driver License: Series")
    driver_license_number = fields.Char(string="Driver License: №")
    is_leave_allowed = fields.Boolean(string="Is leave allowed")
    acts_on_the_basis = fields.Char(string="Acts On The Basis")
