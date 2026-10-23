from odoo import api, fields, models


class Company(models.Model):
    _inherit = "res.company"

    kpp = fields.Char(string="KPP")
    ogrnip = fields.Char(string="OGRNIP")
    okpo = fields.Char(string="OKPO")
    okato = fields.Char(string="OKATO")
    registry_info = fields.Char(string="Registry info")
