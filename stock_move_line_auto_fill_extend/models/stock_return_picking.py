from odoo import models
from odoo import SUPERUSER_ID


class ReturnPicking(models.TransientModel):
    _inherit = 'stock.return.picking'

    def create_returns(self):
        res = super(ReturnPicking, self).create_returns()
        if self.picking_id.picking_type_code == 'incoming':
            return res
        if res.get('res_id'):
            return_picking_id = self.env['stock.picking'].browse(res.get('res_id'))
            for move_id in return_picking_id.move_ids_without_package:
                if move_id.has_tracking != 'none' and move_id.origin_returned_move_id:
                    #delete existing move lines without lot id
                    returned_move_line_ids = self.env['stock.move.line'].search([('move_id', '=', move_id.id)])
                    returned_move_line_ids.unlink()

                    #create new movelines with lot id for return
                    origin_move_line_ids = self.env['stock.move.line'].search([('move_id', '=', move_id.origin_returned_move_id.id)])
                    for origin_move_line in origin_move_line_ids:
                        return_lot_id = self.env['stock.production.lot'].search([('product_id', '=', origin_move_line.product_id.id), ('name', '=', origin_move_line.lot_id.name), ('company_id', '=', move_id.company_id.id)])
                        if return_lot_id:
                            move_line_vals = {
                                'company_id': return_picking_id.company_id.id,
                                'picking_id': return_picking_id.id,
                                'move_id': move_id.id,
                                'product_id': origin_move_line.product_id.id,
                                'location_id': move_id.location_id.id,
                                'location_dest_id': move_id.location_dest_id.id,
                                'lot_id': return_lot_id.id,
                                'lot_name': return_lot_id.name,
                                'qty_done': origin_move_line.qty_done,
                                'product_uom_qty': origin_move_line.qty_done,
                                'product_uom_id': origin_move_line.product_uom_id.id
                                }
                            self.env['stock.move.line'].create(move_line_vals)
            if return_picking_id.state == 'confirmed':
                return_picking_id.action_assign()

        self = self.with_user(SUPERUSER_ID)
        purchase_order_id = self.env['purchase.order'].search([('partner_ref', '=', self.picking_id.origin)])
        if purchase_order_id:
            for picking_id in purchase_order_id.picking_ids:
                if picking_id.state == 'cancel' or (picking_id.picking_type_code == 'incoming' and picking_id.picking_type_id.sequence_code != 'DS'):
                    continue
                vals = {
                    'picking_id': picking_id.id,
                    'location_id': picking_id.location_id.id
                }
                return_wizard = self.env['stock.return.picking'].with_context(
                    active_id=self.picking_id.id).sudo().create(vals)
                lines = []
                for l in self.product_return_moves:
                    if l.quantity == 0.0:
                        continue
                    move_id = self.env['stock.move'].sudo().search(
                        [('product_id', '=', l.product_id.id),
                         ('picking_id', '=', picking_id.id)])
                    if not move_id:
                        continue
                    r_line = self.env['stock.return.picking.line'].sudo().create(
                        {'product_id': l.product_id.id, 'quantity': l.quantity, 'wizard_id': return_wizard.id,
                         'move_id': move_id.id})
                    lines.append(r_line.id)
                if lines:
                    new_picking, pick_type_id = return_wizard.sudo()._create_returns()
                    return_picking_id = self.env['stock.picking'].browse(new_picking)
                    for move_id in return_picking_id.move_ids_without_package:
                        if move_id.has_tracking != 'none' and move_id.origin_returned_move_id:

                            #delete existing move lines without lot id
                            returned_move_line_ids = self.env['stock.move.line'].search([('move_id', '=', move_id.id)])
                            returned_move_line_ids.unlink()

                            #create new movelines with lot id for return
                            origin_move_line_ids = self.env['stock.move.line'].search([('move_id', '=', move_id.origin_returned_move_id.id)])
                            for origin_move_line in origin_move_line_ids:
                                return_lot_id = self.env['stock.production.lot'].search([('product_id', '=', origin_move_line.product_id.id), ('name', '=', origin_move_line.lot_id.name), ('company_id', '=', move_id.company_id.id)])
                                if return_lot_id:
                                    move_line_vals = {
                                        'company_id': return_picking_id.company_id.id,
                                        'picking_id': return_picking_id.id,
                                        'move_id': move_id.id,
                                        'product_id': origin_move_line.product_id.id,
                                        'location_id': move_id.location_id.id,
                                        'location_dest_id': move_id.location_dest_id.id,
                                        'lot_id': return_lot_id.id,
                                        'lot_name': return_lot_id.name,
                                        'qty_done': origin_move_line.qty_done,
                                        'product_uom_qty': origin_move_line.qty_done,
                                        'product_uom_id': origin_move_line.product_uom_id.id
                                        }
                                    self.env['stock.move.line'].create(move_line_vals)
                    if return_picking_id.state == 'confirmed':
                        return_picking_id.action_assign()
                        if return_picking_id.state == 'assigned':
                            return_picking_id.button_validate()
                    break
        return res
