# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = "res.partner"

    statement_account_email = fields.Char(
        string="Statement of Account Email"
    )
