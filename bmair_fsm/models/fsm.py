# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _
from odoo.osv import expression
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError
from odoo.tools import float_compare, float_round

class Task(models.Model):
    _inherit = "project.task"
    
    machine_id = fields.Many2one('fsm.machine.customer', 'Machine',)
    
    def _fsm_create_sale_order(self):
        """ Create the SO from the task, with the 'service product' sales line and link all timesheet to that line it """
        if not self.partner_id:
            raise UserError(_('The FSM task must have a customer set to be sold.'))

        SaleOrder = self.env['sale.order']
        if self.user_has_groups('project.group_project_user'):
            SaleOrder = SaleOrder.sudo()

        domain = ['|', ('company_id', '=', False), ('company_id', '=', self.company_id.id)]
        team = self.env['crm.team'].sudo()._get_default_team_id(domain=domain)
        sale_order = SaleOrder.create({
            'partner_id': self.partner_id.id,
            'company_id': self.company_id.id,
            'analytic_account_id': self.project_id.analytic_account_id.id,
            'team_id': team.id if team else False
        })
        sale_order.onchange_partner_id()

        # write after creation since onchange_partner_id sets the current user
        if self.user_id and self.user_id.default_warehouse:
            warehouse_id = self.user_id and self.user_id.default_warehouse.id
            sale_order.write({'warehouse_id': warehouse_id})
        sale_order.write({'user_id': self.user_id.id})

        self.sale_order_id = sale_order
        
    def action_fsm_view_material(self):
        self._fsm_ensure_sale_order()

        domain = [('sale_ok', '=', True), '|', ('company_id', '=', self.company_id.id), ('company_id', '=', False)]
        if self.project_id and self.project_id.timesheet_product_id:
            domain = expression.AND([domain, [('id', '!=', self.project_id.timesheet_product_id.id)]])
        deposit_product = self.env['ir.config_parameter'].sudo().get_param('sale.default_deposit_product_id')
        if deposit_product:
            domain = expression.AND([domain, [('id', '!=', deposit_product)]])
        if not self.user_id:
            error_msg = _('Please add user before selecting product')
            raise UserError(error_msg)
        if self.user_id and not self.user_id.default_warehouse:
            error_msg = _('Please add default warehouse to user before selecting product')
            raise UserError(error_msg)
        if self.user_id and self.user_id.default_warehouse:
            domain = expression.AND([domain, [('id', '!=', deposit_product)]])
            quant_ids = self.env['stock.quant'].search([('location_id', 'child_of', self.user_id.default_warehouse.lot_stock_id.id)])
            product_list = []
            for quant in quant_ids:
                if quant.product_id and quant.product_id.id not in product_list:
                    product_list.append(quant.product_id.id)
#             if product_list:
            domain = expression.AND([domain, [('id', 'in', product_list)]])
        print (domain, "ddddddddddddddd")
        kanban_view = self.env.ref('industry_fsm_sale.view_product_product_kanban_material')
        return {
            'type': 'ir.actions.act_window',
            'name': _('Choose Products'),
            'res_model': 'product.product',
            'views': [(kanban_view.id, 'kanban'), (False, 'form')],
            'domain': domain,
            'context': {
                'fsm_mode': True,
#                 'create': self.env['product.template'].check_access_rights('create', raise_exception=False),
                'fsm_task_id': self.id,  # avoid 'default_' context key as we are going to create SOL with this context
                'pricelist': self.partner_id.property_product_pricelist.id if self.partner_id else False,
                'partner': self.partner_id.id if self.partner_id else False,
                'search_default_consumable': 1,
                'hide_qty_buttons': self.fsm_done
            },
            'help': _("""<p class="o_view_nocontent_smiling_face">
                            Create a new product
                        </p><p>
                            You must define a product for everything you sell or purchase,
                            whether it's a storable product, a consumable or a service.
                        </p>""")
        }
        #to find fms product list
    def fsm_material_list(self):
        self._fsm_ensure_sale_order()
        product_list = []
        domain = [('sale_ok', '=', True), '|', ('company_id', '=', self.company_id.id), ('company_id', '=', False)]
        if self.project_id and self.project_id.timesheet_product_id:
            domain = expression.AND([domain, [('id', '!=', self.project_id.timesheet_product_id.id)]])
        deposit_product = self.env['ir.config_parameter'].sudo().get_param('sale.default_deposit_product_id')
        if deposit_product:
            domain = expression.AND([domain, [('id', '!=', deposit_product)]])
        if not self.user_id:
            error_msg = _('Please add user before selecting product')
            raise UserError(error_msg)
        if self.user_id and not self.user_id.default_warehouse:
            error_msg = _('Please add default warehouse to user before selecting product')
            raise UserError(error_msg)
        if self.user_id and self.user_id.default_warehouse:
            domain = expression.AND([domain, [('id', '!=', deposit_product)]])
            quant_ids = self.env['stock.quant'].search([('location_id', 'child_of', self.user_id.default_warehouse.lot_stock_id.id)])
            for quant in quant_ids:
                if quant.product_id and quant.product_id.id not in product_list:
                    product_list.append(quant.product_id)
            domain = expression.AND([domain, [('id', 'in', product_list)]])
        return product_list
    
    def compute_fsm_quantity(self, product_list):
            final_list = []
            SaleOrderLine = self.env['sale.order.line']
            task = self.sudo()
            SaleOrderLine = SaleOrderLine.sudo()

            products_qties = SaleOrderLine.read_group(
                [('id', 'in', task.sale_order_id.order_line.ids), ('task_id', '=', task.id)],
                ['product_id', 'product_uom_qty'], ['product_id'])
            qty_dict = dict([(x['product_id'][0], x['product_uom_qty']) for x in products_qties if x['product_id']])
            for product in product_list:
                product.fsm_quantity = qty_dict.get(product.id, 0)
                if product.fsm_quantity > 0:
                    final_list.append(product.id)
            return final_list
    
        # code change to make changes in source location , same as technician  location
    def _validate_stock(self):
        self.ensure_one()
        all_fsm_sn_moves = self.env['stock.move']
        ml_to_create = []
        for so_line in self.sale_order_id.order_line:
            qty = so_line.product_uom_qty - so_line.qty_delivered
            fsm_sn_moves = self.env['stock.move']
            if not qty:
                continue
            for last_move in so_line.move_ids.filtered(lambda p: p.state not in ['done', 'cancel']):
                move = last_move
                fsm_sn_moves |= last_move
                while move.move_orig_ids:
                    move = move.move_orig_ids
                    fsm_sn_moves |= move
            for fsm_sn_move in fsm_sn_moves:
                print ("fsm_sn_move---",fsm_sn_move)
                ml_vals = fsm_sn_move._prepare_move_line_vals(quantity=0)
                ml_vals['qty_done'] = qty
                ml_vals['lot_id'] = so_line.fsm_lot_id.id
                #adding fms user location 
                if self.user_id.default_warehouse and self.user_id.default_warehouse.lot_stock_id:
                    if ml_vals['product_id'] in self.compute_fsm_quantity(self.fsm_material_list()):
                        ml_vals['location_id'] = self.user_id.default_warehouse.lot_stock_id.id
                ml_to_create.append(ml_vals)
            all_fsm_sn_moves |= fsm_sn_moves
        self.env['stock.move.line'].create(ml_to_create)

        pickings_to_do = self.sale_order_id.picking_ids.filtered(lambda p: p.state not in ['done', 'cancel'])
        
        for move in pickings_to_do.move_lines:
            if move.state in ('done', 'cancel') or move in all_fsm_sn_moves:
                continue
            rounding = move.product_uom.rounding
            if float_compare(move.quantity_done, move.product_uom_qty, precision_rounding=rounding) < 0:
                qty_to_do = float_round(
                    move.product_uom_qty - move.quantity_done,
                    precision_rounding=rounding,
                    rounding_method='HALF-UP')
                move._set_quantity_done(qty_to_do)
        
        pickings_to_do.with_context(skip_sms=True, cancel_backorder=True).button_validate()
