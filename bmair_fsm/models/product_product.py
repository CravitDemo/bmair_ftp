# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, _
from odoo.exceptions import UserError

class ProductProduct(models.Model):
    _inherit = 'product.product'


    def _inverse_fsm_quantity(self):
        task = self._get_contextual_fsm_task()
        if task:
            for product in self:
                sale_lines = self.env['sale.order.line'].search(
                    [('order_id', '=', task.sale_order_id.id), ('product_id', '=', product.id),
                     ('task_id', '=', task.id)])
                all_editable_lines = sale_lines.filtered(lambda
                                                             l: l.qty_delivered == 0 or l.qty_delivered_method == 'manual' or l.state not in [
                    'sale', 'done'])
                diff_qty = product.fsm_quantity - sum(sale_lines.mapped('product_uom_qty'))
                if all_editable_lines:  # existing line: change ordered qty (and delivered, if delivered method)
                    if diff_qty > 0:
                        if task.user_id and not task.user_id.route_id:
                            raise UserError(
                                _("Please define FSM Route for the user: %s!") % (task.user_id.name))
                        all_editable_lines[0].with_context(fsm_no_message_post=True).write({
                            'product_uom_qty': all_editable_lines[0].product_uom_qty + diff_qty,
                            'route_id': task.user_id.route_id.id,
                        })
                        continue
                    # diff_qty is negative, we remove the quantities from existing editable lines:
                    for line in all_editable_lines:
                        new_line_qty = max(0, line.product_uom_qty + diff_qty)
                        diff_qty += line.product_uom_qty - new_line_qty
                        line.product_uom_qty = new_line_qty

                        #update qty in related picking
                        move_id = self.env['stock.move'].search([('sale_line_id', '=', line.id)])
                        if move_id and move_id.picking_id.state not in ['done', 'cancel']:
                            flag = False
                            if move_id.picking_id.state == 'assigned':
                                move_id.picking_id.do_unreserve()
                                flag = True
                            move_id.product_uom_qty = new_line_qty
                            if flag:
                                move_id.picking_id.action_assign()

                        if diff_qty == 0:
                            break
                elif diff_qty > 0:  # create new SOL
                    if task.user_id and not task.user_id.route_id:
                        raise UserError(
                            _("Please define FSM Route for the user: %s!") % (task.user_id.name))
                    vals = {
                        'order_id': task.sale_order_id.id,
                        'product_id': product.id,
                        'product_uom_qty': diff_qty,
                        'product_uom': product.uom_id.id,
                        'task_id': task.id,
                        'route_id': task.user_id.route_id.id,
                    }
                    if task.sale_order_id.pricelist_id.discount_policy == 'without_discount':
                        sol = self.env['sale.order.line'].new(vals)
                        sol._onchange_discount()
                        vals.update({'discount': sol.discount or 0.0})
                    sale_line = self.env['sale.order.line'].create(vals)