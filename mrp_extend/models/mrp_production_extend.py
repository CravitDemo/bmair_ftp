# -*- coding: utf-8 -*-

import datetime
from odoo import api, fields, models, _

                
class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'             

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        mo_id = False
        if self.env.context.get('default_production'):
            mo_id =self.env['mrp.production'].browse(self.env.context['default_production'])
        if self.env.context.get('active_mo_id'):
            mo_id =self.env['mrp.production'].browse(self.env.context['active_mo_id'])

        if  mo_id and self.env.context.get('default_product_id'):
            prod_id = self.env['product.product'].browse(self.env.context['default_product_id'])
            if mo_id.lot_producing_id and prod_id.id == mo_id.product_id.id:
                args.append((('id','in',[mo_id.lot_producing_id.id])))
            elif prod_id.id != mo_id.product_id.id:
                for raw_id in mo_id.move_raw_ids:
                    if raw_id.product_id == prod_id:
                        args.append((('id','in',raw_id.move_line_ids.mapped('lot_id').ids)))
            else:
                args.append((('id','in',[])))
        ids = self._name_search(name, args, operator, limit=limit)
        return self.browse(ids).sudo().name_get()

'''class mrpproduction(models.Model):
    _inherit = "mrp.production"

    def action_generate_backorder_wizard(self):
        """ Opens a wizard to assign SN's name on each move lines.
        """
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id("mrp_extend.act_assign_serial_numbers_mo")
        action['context'] = {
            'default_product_id': self.product_id.id,
            'default_mo_id': self.id,
        }
        return action'''

