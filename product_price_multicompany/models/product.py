# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    list_price = fields.Html('Verkooporder Omschrijving')

    list_price = fields.Float(
        'Sales Price', default=1.0,
        digits='Product Price',
        help="Price at which the product is sold to customers.",
        company_dependent=True)
    # lst_price: catalog price for template, but including extra for variants
    lst_price = fields.Float(
        'Public Price', related='list_price', readonly=False,
        digits='Product Price', company_dependent=True)
