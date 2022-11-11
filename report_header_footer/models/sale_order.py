# -*- coding: utf-8 -*-

from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def convert_price(self, amount):
        if str(amount).find(".") != -1:
            amount = str(amount).replace(".", ",")
        return amount
