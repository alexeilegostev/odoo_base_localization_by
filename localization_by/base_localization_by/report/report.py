# -*- coding: utf-8 -*-
from odoo import models, api
from .report_helper import QWebHelper


class AcceptanceReport(models.AbstractModel):
    _name = "report.base_localization_by.acceptance_report"
    _description = "Acceptance report"

    @api.model
    def _get_report_values(self, doc_ids, data=None):
        """Prepare data for acceptance report of Act. In report shouldn't be Down Payment Lines"""
        docs = self.env["account.move"].browse(doc_ids)
        account_move_data = get_prepared_account_move_data(self, docs)
        company_id = self.env.user.company_id
        doc_args = {
            "company_id": company_id,
            "doc_model": "account.move",
            "docs": docs,
            "account_move_data": account_move_data,
            "helper": QWebHelper(),
            "proforma": True
        }
        return doc_args


class ReportAccountProtocolInv(models.AbstractModel):
    _name = "report.base_localization_by.account_protocol_inv"
    _description = "Report for account-protocol from invoice"

    @api.model
    def _get_report_values(self, doc_ids, data=None):
        """Prepare data for acceptance report of Invoice-protocol. In report shouldn't be Down Payment Lines"""
        docs = self.env["account.move"].browse(doc_ids)
        account_move_data = get_prepared_account_move_data(self, docs)
        company_id = self.env.user.company_id
        doc_args = {
            "company_id": company_id,
            "doc_ids": docs.ids,
            "doc_model": "account.move",
            "docs": docs,
            "account_move_data": account_move_data,
            "helper": QWebHelper(),
            "proforma": True
        }
        return doc_args


class ReportAccountProtocolPick(models.AbstractModel):
    _name = "report.base_localization_by.account_protocol_pick"
    _description = "Report for account-protocol from picking"

    @api.model
    def _get_report_values(self, doc_ids, data=None):
        """Prepare data for acceptance report of picking."""
        docs = self.env["stock.picking"].browse(doc_ids)
        account_move_data = get_prepared_account_move_data(self, docs)
        company_id = self.env.user.company_id
        doc_args = {
            "company_id": company_id,
            "doc_ids": docs.ids,
            "doc_model": "stock.picking",
            "docs": docs,
            "account_move_data": account_move_data,
            "helper": QWebHelper(),
            "proforma": True
        }
        return doc_args


class ReportSpecificationInv(models.AbstractModel):
    _name = "report.base_localization_by.specification_inv"
    _description = "Report for specification from invoice"

    @api.model
    def _get_report_values(self, doc_ids, data=None):
        """Prepare data for acceptance report of Specification. In report shouldn't be Down Payment Lines"""
        docs = self.env["account.move"].browse(doc_ids)
        account_move_data = get_prepared_account_move_data(self, docs)
        company_id = self.env.user.company_id
        doc_args = {
            "company_id": company_id,
            "doc_ids": docs.ids,
            "doc_model": "account.move",
            "docs": docs,
            "account_move_data": account_move_data,
            "helper": QWebHelper(),
            "proforma": True
        }
        return doc_args


class ReportSpecificationPick(models.AbstractModel):
    _name = "report.base_localization_by.specification_pick"
    _description = "Report for specification from picking"

    @api.model
    def _get_report_values(self, docids, data=None):
        """Prepare data for acceptance report of picking."""
        docs = self.env["stock.picking"].browse(docids)
        # partner = docs.mapped("partner_id")
        company_id = self.env.user.company_id
        docargs = {
            "company_id": company_id,
            "doc_ids": docs.ids,
            "doc_model": "stock.picking",
            "docs": docs,
            "helper": QWebHelper(),
            "proforma": True
        }
        return docargs


class ReportTtnVerticalInv(models.AbstractModel):
    _name = "report.base_localization_by.report_ttn_vertical_inv"
    _description = "Report for TTN from invoice"

    @api.model
    def _get_report_values(self, doc_ids, data=None):
        """Prepare data for acceptance report of TTN. In report shouldn't be Down Payment Lines"""
        docs = self.env["account.move"].browse(doc_ids)
        account_move_data = get_prepared_account_move_data(self, docs)
        company_id = self.env.user.company_id
        doc_args = {
            "company_id": company_id,
            "doc_ids": docs.ids,
            "doc_model": "account.move",
            "docs": docs,
            "account_move_data": account_move_data,
            "helper": QWebHelper(),
            "proforma": True
        }
        return doc_args


class ReportTtnHorizontalInv(ReportTtnVerticalInv):
    _name = "report.base_localization_by.report_ttn_horizontal_inv"


class ReportTtnWithAttachmentVerticalInv(ReportTtnVerticalInv):
    _name = "report.base_localization_by.report_ttn_with_attach_vert_inv"


class ReportTtnWithAttachmentHorizontalInv(ReportTtnVerticalInv):
    _name = "report.base_localization_by.report_ttn_with_attach_horiz_inv"


class ReportTtnVerticalPick(models.AbstractModel):
    _name = "report.base_localization_by.report_ttn_vertical_pick"
    _description = "Report for TTN from picking"

    @api.model
    def _get_report_values(self, docids, data=None):
        """Prepare data for acceptance report of TTN picking."""
        docs = self.env["stock.picking"].browse(docids)
        company_id = self.env.user.company_id
        docargs = {
            "company_id": company_id,
            "doc_ids": docs.ids,
            "doc_model": "stock.picking",
            "docs": docs,
            "helper": QWebHelper(),
            "proforma": True
        }
        return docargs


class ReportTtnHorizontalPick(ReportTtnVerticalPick):
    _name = "report.base_localization_by.report_ttn_horizontal_pick"


class ReportTtnWithAttachmentVerticalPick(ReportTtnVerticalPick):
    _name = "report.base_localization_by.report_ttn_with_attach_vert_pick"


class ReportTtnWithAttachmentHorizontalPick(ReportTtnVerticalPick):
    _name = "report.base_localization_by.report_ttn_with_attach_horiz_pick"


class ReportTnVerticalInv(models.AbstractModel):
    _name = "report.base_localization_by.report_tn_vertical_inv"
    _description = "Report for TN from invoice"

    @api.model
    def _get_report_values(self, doc_ids, data=None):
        """Prepare data for acceptance report of TN. In report shouldn't be Down Payment Lines"""
        docs = self.env["account.move"].browse(doc_ids)
        account_move_data = get_prepared_account_move_data(self, docs)
        company_id = self.env.user.company_id
        doc_args = {
            "company_id": company_id,
            "doc_ids": docs.ids,
            "doc_model": "account.move",
            "docs": docs,
            "account_move_data": account_move_data,
            "helper": QWebHelper(),
            "proforma": True
        }
        return doc_args


class ReportTnHorizontalInv(ReportTnVerticalInv):
    _name = "report.base_localization_by.report_tn_horizontal_inv"


class ReportTnWithAttachVerticalInv(ReportTnVerticalInv):
    _name = "report.base_localization_by.report_tn_with_attach_vert_inv"


class ReportTnWithAttachHorizontalInv(ReportTnVerticalInv):
    _name = "report.base_localization_by.report_tn_with_attach_horiz_inv"


class ReportTnVerticalPick(models.AbstractModel):
    _name = "report.base_localization_by.report_tn_vertical_pick"
    _description = "Report for TN from picking"

    @api.model
    def _get_report_values(self, docids, data=None):
        """Prepare data for acceptance report of TN."""
        docs = self.env["stock.picking"].browse(docids)
        company_id = self.env.user.company_id
        docargs = {
            "company_id": company_id,
            "doc_ids": docs.ids,
            "doc_model": "stock.picking",
            "docs": docs,
            "helper": QWebHelper(),
            "proforma": True
        }
        return docargs


class ReportTnHorizontalPick(ReportTnVerticalPick):
    _name = "report.base_localization_by.report_tn_horizontal_pick"


class ReportTnWithAttachVerticalPick(ReportTnVerticalPick):
    _name = "report.base_localization_by.report_tn_with_attach_vert_pick"


class ReportTnWithAttachHorizontalPick(ReportTnVerticalPick):
    _name = "report.base_localization_by.report_tn_with_attach_horiz_pick"


def get_prepared_account_move_data(self, docs):
    """
    Prepare additional data for report.

    :param self: object of Model
    :type self: model.Model
    :param docs: recordset of invoices
    :type docs: recordset
    :return: dict of prepared data
    :rtype: dictionary
    """
    deposit_param = self.env.get("ir.config_parameter").sudo().get_param("sale.default_deposit_product_id", False)
    account_move_data = dict()
    for doc in docs:
        param_data = dict()
        if doc._name == "stock.picking":
            lines = doc.move_ids_without_package
        else:
            if deposit_param:
                lines = doc.invoice_line_ids.filtered(lambda rec: rec.product_id.id != int(deposit_param))
            else:
                lines = doc.invoice_line_ids
        param_data["invoice_lines"] = lines
        param_data["currency_id"] = doc.currency_id or doc.env.company.currency_id
        param_data["price_tax"] = sum(lines.mapped("price_tax"))
        param_data["amount_total"] = sum(lines.mapped("price_total"))
        param_data["cargo_places"] = sum(lines.mapped("cargo_places"))
        param_data["weight"] = sum(lines.mapped("weight"))
        account_move_data[doc.id] = param_data
    return account_move_data
