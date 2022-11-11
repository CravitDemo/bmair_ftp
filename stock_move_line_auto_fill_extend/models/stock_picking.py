from odoo import models
from odoo import SUPERUSER_ID


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def button_validate(self):
        res = super(StockPicking, self).button_validate()
        if type(res) == bool and self.sale_id and self.sale_id.auto_purchase_order_id:
            self = self.with_user(SUPERUSER_ID)
            dropship = self.search([('origin', '=', self.sale_id.auto_purchase_order_id.name)], limit=1)
            if dropship.state == 'done':
                dropship = self.search([('origin', 'ilike', dropship.name)], limit=1)
            if dropship:
                for line in self.move_line_ids_without_package:
                    for drop_line in dropship.move_line_ids_without_package:
                        if line.product_id == drop_line.product_id:
                            if not drop_line.lot_id and not line.lot_id and drop_line.product_id.tracking == 'none':
                                drop_line.write(
                                    {'qty_done': line.qty_done, 'intercompany_moveline_id': line.id})
                                break
                            if not drop_line.lot_id and line.lot_id:
                                lot_id = self.env['stock.production.lot'].search([('product_id', '=', line.product_id.id), ('name', '=', line.lot_id.name), ('company_id', '=', dropship.company_id.id)], limit=1)
                                if not lot_id:
                                    lot_id = self.env['stock.production.lot'].create({
                                                                'name': line.lot_id.name,
                                                                'product_id': line.product_id.id,
                                                                'product_qty': line.product_uom_qty,
                                                                'product_uom_id': line.product_uom_id.id,
                                                                'company_id': dropship.company_id.id
                                                                })
                                drop_line.write({'lot_id': lot_id.id, 'qty_done': line.qty_done, 'intercompany_moveline_id': line.id})
                                break
                if dropship.state == 'assigned':
                    dropship.button_validate()
        return res
