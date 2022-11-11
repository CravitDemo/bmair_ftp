# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError


class FsmStockTracking(models.TransientModel):
    _inherit = 'fsm.stock.tracking'

    def generate_lot(self):
        if self.fsm_done:
            return

        if self.tracking_line_ids.filtered(lambda l: not l.lot_id):
            raise UserError(_('Each line needs a Lot/Serial Number'))

        SaleOrderLine = self.env['sale.order.line'].sudo()

        sale_lines_remove = SaleOrderLine.search([
            ('order_id', '=', self.task_id.sale_order_id.id),
            ('product_id', '=', self.product_id.id),
            ('id', 'not in', self.tracking_line_ids.sale_order_line_id.ids),
            ('task_id', '=', self.task_id.id)
        ])

        for line in self.tracking_line_ids:
            qty = line.quantity if self.tracking == 'lot' else 1
            if line.sale_order_line_id:
                line.sale_order_line_id.write({'fsm_lot_id': line.lot_id, 'route_id': self.task_id.user_id.route_id.id, 'product_uom_qty': qty + line.sale_order_line_id.qty_delivered})
            elif qty:
                vals = {
                    'order_id': self.task_id.sale_order_id.id,
                    'product_id': self.product_id.id,
                    'product_uom_qty': qty,
                    'product_uom': self.product_id.uom_id.id,
                    'task_id': self.task_id.id,
                    'fsm_lot_id': line.lot_id.id,
                    'route_id': self.task_id.user_id.route_id.id,
                }
                SaleOrderLine.create(vals)

        if self.task_id.sale_order_id.state == 'draft':
            sale_lines_remove.unlink()
        else:
            for sl in sale_lines_remove:
                sl.write({'product_uom_qty': sl.qty_delivered})
