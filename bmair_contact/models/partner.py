# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Resham Kumari - B-informed B.V.
#    Copyright 2016 B-informed B.V.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.osv import expression
import re
from math import pi 
import math
import requests
import json
import logging
import base64
from odoo.exceptions import UserError
from random import randint
_logger = logging.getLogger(__name__)

class PartnerBrand(models.Model):
    _description = 'Partner Brand'
    _name = 'res.partner.brand'
    _order = 'name'

#     def _get_default_color(self):
#         return randint(1, 11)
    
    name = fields.Char(string='Name', required=True, translate=True)
    active = fields.Boolean(default=True, help="The active field allows you to hide the partner brand without removing it.")
    partner_ids = fields.Many2many('res.partner', column1='brand_id', column2='partner_id', string='Partners')
#     color = fields.Integer(string='Color Index', default=_get_default_color)

class ResPartnerType(models.Model):

    _name = "res.partner.type"
    _description = "Customer Type"

    name = fields.Char(string="Name", required=True, translate=True)
    active = fields.Boolean(default=True, help="The active field allows you to hide the partner type without removing it.")
#     shortcut = fields.Char(string="Abbreviation", translate=True)

    _sql_constraints = [
        ("name_uniq", "unique (name)", "Customer Type already exists!")
    ]

class ResPartner(models.Model):
    _inherit = "res.partner"
    
    def _default_brand(self):
        return self.env['res.partner.brand'].browse(self._context.get('brand_ids'))
    
    mamut_nr = fields.Char(string="Mamut Nr")
    partner_type_id = fields.Many2one(
        comodel_name="res.partner.type", string="Customer Type"
    )
    ref = fields.Char(string='Order Reference', readonly= True, copy=False, index=True, default=lambda self: _('New'))
    brand_ids = fields.Many2many('res.partner.brand', column1='partner_id',
                                    column2='brand_id', string='Customer Brand', default=_default_brand)
    
    @api.model
    def create(self, vals):
        if 'company_id' in vals:
            self = self.with_company(vals['company_id'])
        if vals.get('ref', _('New')) == _('New') and 'company_type' in vals and vals['company_type']== 'company':
            vals['ref'] = self.env['ir.sequence'].next_by_code('res.partner') or _('')
        if vals.get('ref', _('New')) == _('New') and 'company_type' in vals and vals['company_type'] != 'company':
            vals['ref'] = ''
        result = super(ResPartner, self).create(vals)
        return result