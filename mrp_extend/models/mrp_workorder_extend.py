# -*- coding: utf-8 -*-

import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError

                
class MrpProductionWorkcenterLine(models.Model):
    _inherit = 'mrp.workorder'

    def button_start(self):
        if self.production_id.product_id.tracking != 'none' and not self.production_id.lot_producing_id:
            raise UserError(_("Assign Lot/Serial Number before starting workorder! "))
        res = super().button_start()
        if self.product_tracking == 'serial' and self.component_id:
            self._update_component_quantity()
        return res

    def open_tablet_view(self):
        if self.production_id.product_id.tracking != 'none' and not self.production_id.lot_producing_id:
            raise UserError(_("Assign Lot/Serial Number before processing workorder! "))
        self.ensure_one()
        if not self.is_user_working and self.working_state != 'blocked' and self.state in ('ready', 'progress', 'pending'):
            self.button_start()
        return {
                'type': 'ir.actions.act_window',
                'res_model': 'mrp.workorder',
                'views': [[self.env.ref('mrp_workorder.mrp_workorder_view_form_tablet').id, 'form']],
                'res_id': self.id,
                'target': 'fullscreen',
                'flags': {
                    'withControlPanel': False,
                    'form_view_initial_mode': 'edit',
                },
                'context': {'from_production_order': self.env.context.get('from_production_order')},
            }       
