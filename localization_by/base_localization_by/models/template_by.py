from odoo import models, _
from odoo.addons.account.models.chart_template import template


class AccountChartTemplate(models.AbstractModel):
    _inherit = "account.chart.template"

    @template("by")
    def _get_by_template_date(self):
        """Template data for Belarus localization (типовой план счетов)."""
        return {
            "property_account_receivable_id": "by_account_62",
            "property_account_payable_id": "by_account_60",
            "property_account_expense_categ_id": "by_account_9003",
            "property_account_income_categ_id": "by_account_9001",
            "property_stock_account_input_categ_id": "by_account_15",
            "property_stock_account_output_categ_id": "by_account_45",
            "property_stock_valuation_account_id": "by_account_41",
            "income_currency_exchange_account_id": "by_account_9101",
            "deferred_revenue_account_id": "by_account_98",
            "expense_currency_exchange_account_id": "by_account_9102",
            "default_cash_difference_income_account_id": "by_account_9101",
            "default_cash_difference_expense_account_id": "by_account_9102",
            "default_pos_receivable_account_id": "by_account_6203",
            "account_journal_early_pay_discount_gain_account_id": "by_account_9101",
            "account_journal_early_pay_discount_loss_account_id": "by_account_9102",
            "name": _("Belarus - Chart of Accounts"),
            "code_digits": "4",
        }

    @template("by", "res.company")
    def _get_by_res_company(self):
        """Company defaults for Belarus localization."""
        return {
            self.env.company.id: {
                "anglo_saxon_accounting": True,
                "account_fiscal_country_id": "base.by",
                "bank_account_code_prefix": "51",
                "cash_account_code_prefix": "50",
                "transfer_account_code_prefix": "57",
                "account_sale_tax_id": "sale_tax_template_20",
                "account_purchase_tax_id": "purchase_tax_template_20",
            }
        }

    @template(model="product.product")
    def _get_product_product(self, template_code):
        """Add advance products when the fiscal localization is applied."""
        return self._parse_csv(template_code, "product.product")

    @template("by", "res.company")
    def _get_by_default_settings(self):
        """Link default deposit products after chart loading."""
        company = self.env.company
        sale_account = self.env["account.account"].search([
            ("company_id", "=", company.id),
            ("code", "=", "6202"),
        ], limit=1)
        purchase_account = self.env["account.account"].search([
            ("company_id", "=", company.id),
            ("code", "=", "6002"),
        ], limit=1)

        values = {}
        if purchase_account:
            purchase_deposit = self.env["product.product"].search([
                ("company_id", "=", company.id),
                "|",
                ("property_account_income_id", "=", purchase_account.id),
                ("property_account_expense_id", "=", purchase_account.id),
            ], limit=1)
            if purchase_deposit and "purchase_deposit_product_id" in company._fields:
                values["purchase_deposit_product_id"] = purchase_deposit.id
        if sale_account:
            sale_deposit = self.env["product.product"].search([
                ("company_id", "=", company.id),
                "|",
                ("property_account_income_id", "=", sale_account.id),
                ("property_account_expense_id", "=", sale_account.id),
            ], limit=1)
            if sale_deposit and "sale_deposit_product_id" in company._fields:
                values["sale_deposit_product_id"] = sale_deposit.id

        return {company.id: values} if values else {}
