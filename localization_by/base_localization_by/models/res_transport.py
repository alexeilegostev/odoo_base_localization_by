from odoo import models, fields, api, _


class ResTransport(models.Model):
    _inherit = "res.transport"

    driver_employee_id = fields.Many2one(
        comodel_name="res.partner",
        string="Default Driver",
        domain="[('is_driver', '=', True)]",
    )
