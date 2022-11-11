# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models

class BmairHistory(models.Model):
    _name = 'bmair.history'
    _description = 'BMair History'
    _rec_name = 'field_name'
    _order = 'id desc'
    
    sel_model = fields.Selection([('sale_order', 'Sale Order'), ('so_line', 'Sale Order Line'), ('bom', 'Bill Of Material'),
                                ('product', 'Product'),('mrp_bom_line', 'BOM Line'),('mrp_routing_workcenter', 'MRP Workcenter'),
                                  ('contact', 'Contact'),('partner_bank', 'Partner Bank')], string="Model")
    modification_user_id = fields.Many2one('res.users',string='Modified By')
    old_value = fields.Char(string="Old Value")
    new_value = fields.Char(string="New Value")
    field_name = fields.Char(string="Field")
    record_id = fields.Char(string="Record")
    record_name = fields.Char(string="Name")
    trigger_function = fields.Selection([
        ('create', 'Create'),
        ('write', 'Write'),
        ('delete', 'Delete'),
    ], default='write', string="Trigger Function")
    co_model_name = fields.Char(string="Co-Model Name")
    company_id = fields.Many2one('res.company', string="Company")
    
