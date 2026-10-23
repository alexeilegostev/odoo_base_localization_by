from odoo import models, fields


class EmployeeAccount(models.Model):
    _name = "employee.account"
    _description = "Default bank accounts for employee created from user card"

    account_payable_id = fields.Many2one(comodel_name="account.account", string="Account payable")
    account_receivable_id = fields.Many2one(comodel_name="account.account", string="Account receivable")
