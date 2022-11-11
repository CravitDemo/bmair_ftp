# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class MrpWorkorder(models.Model):
    _inherit = 'mrp.workorder'
    
    wo_responsible_id = fields.Many2one('res.users', 'WO Responsible')
        
        
