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

from odoo import fields, models, api, _
from odoo.osv import expression
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError

class ControllerProduct(models.Model):
    _name = 'product.controller'


    name= fields.Char(String="Name",required=True)
    
class SystemProduct(models.Model):
    _name = 'product.system'


    name= fields.Char(String="Name",required=True)


class FsmMachineCustomer(models.Model):
    _name = "fsm.machine.customer"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Customer Machine'
    
    def name_get(self):
        return list(self._compute_complete_name().items())

    @api.depends('brand_id', 'type', 'chassis_nr')
    def _compute_complete_name(self):
        """ Forms complete name of machine  """
        res = {}
        for machine in self:
            name = machine.brand_id.name
            if machine.type and name:
                name = name + ' / ' +  machine.type     
            if machine.chassis_nr and name:
                name = name + ' / ' +  machine.chassis_nr    
            res[machine.id] = name
            machine.name = name
        return res
    
    name = fields.Char(string='Name', copy=False, compute='_compute_complete_name', store=True, index=True, tracking=True)
    active = fields.Boolean(
        'Active', default=True,
        help="If unchecked, it will allow you to hide the product without removing it.")
    brand_id = fields.Many2one('res.partner.brand', string='Machine Brand',required=True)
    type = fields.Char(string='Machine Type', required=True)
    chassis_nr = fields.Char(string='Chassis Number', required=True)
    construction_year = fields.Char(string='Construction Year')
    product_id = fields.Many2one('product.system', string='System')
    lot_id = fields.Many2one('stock.production.lot', string='System Serial Number')
#     lot_id = fields.Many2one('stock.production.lot', string='System Serial Number',domain=[('product_id', '=', product_id)])
    controllert_id = fields.Many2one('product.controller', string='Controller')
    controllert_number = fields.Char(string='Controller Serial Number',)
    partner_id = fields.Many2one('res.partner', string='Owner', required=True)
    task_count = fields.Integer(compute='_compute_task_count', string="Task Count")
    
    def _compute_task_count(self):
        task_data = self.env['project.task'].read_group([('machine_id', 'in', self.ids), '|', '&', ('stage_id.is_closed', '=', False), ('stage_id.fold', '=', False), ('stage_id', '=', False)], ['machine_id'], ['machine_id'])
        print (task_data,"task_data---")
        result = dict((data['machine_id'][0], data['machine_id_count']) for data in task_data)
        for machine in self:
            machine.task_count = result.get(machine.id, 0)


class ResPartner(models.Model):
    _inherit = 'res.partner'

#     machine_ids = fields.One2many('fsm.machine.customer', 'partner_id', 'Machines')
    machine_count = fields.Integer(compute='_compute_machine_count', string='Machines Count')

    def _compute_machine_count(self):
        # retrieve all children partners and prefetch 'parent_id' on them
        all_partners = self.with_context(active_test=False).search([('id', 'child_of', self.ids)])
        all_partners.read(['parent_id'])

        sale_order_groups = self.env['fsm.machine.customer'].read_group(
            domain=[('partner_id', 'in', all_partners.ids)],
            fields=['partner_id'], groupby=['partner_id']
        )
        partners = self.browse()
        for group in sale_order_groups:
            partner = self.browse(group['partner_id'][0])
            while partner:
                if partner in self:
                    partner.machine_count += group['partner_id_count']
                    partners |= partner
                partner = partner.parent_id
        (self - partners).machine_count = 0  
        
class ProductionLot(models.Model):
    _inherit = 'stock.production.lot'
    
    def name_get(self):
        return list(self._compute_complete_name().items())

    def _compute_complete_name(self):
        """ Forms complete name of location from parent location to child location. """
        res = {}
        for lot in self:
            name = lot.name
            if lot.product_id and name:
                if lot.product_id.default_code:
                    code = lot.product_id.default_code
                    p_name = '[%s] %s' % (code,lot.product_id.name)
                    name = name + ' / '  + p_name      
                else:
                    name = name + ' / '  + lot.product_id.name   
            res[lot.id] = name
        return res
# class Partner(models.Model):
#     _description = 'Contact'
#     _inherit = "res.partner"
#     
#     machine_ids = fields.One2many('fsm.machine.customer', 'partner_id', string="Machines")
