# -*- coding: utf-8 -*-

import datetime
from odoo import api, fields, models, _
from odoo.tools import float_compare, float_round, float_is_zero
from odoo.exceptions import UserError, ValidationError
                
class Picking(models.Model):
    _inherit = "stock.picking"
    
    mo_product_id = fields.Many2one(
        'product.product', 'MO Product',
        readonly=True, related='group_id.mrp_production_ids.product_id', store=True)
    mo_qty = fields.Float(
         'Quantity',
        readonly=True, related='group_id.mrp_production_ids.product_qty', store=True)