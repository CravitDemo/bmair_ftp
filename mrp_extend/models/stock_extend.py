# -*- coding: utf-8 -*-

import datetime
from odoo import api, fields, models, _
from odoo.tools import float_compare, float_round, float_is_zero
from odoo.exceptions import UserError, ValidationError
                
class StockMove(models.Model):
    _inherit = "stock.move"

    def _split(self, qty, restrict_partner_id=False):
        """ Splits `self` quantity and return values for a new moves to be created afterwards

        :param qty: float. quantity to split (given in product UoM)
        :param restrict_partner_id: optional partner that can be given in order to force the new move to restrict its choice of quants to the ones belonging to this partner.
        :returns: list of dict. stock move values """
        self.ensure_one()
        if self.state in ('done', 'cancel'):
            raise UserError(_('You cannot split a stock move that has been set to \'Done\'.'))
        elif self.state == 'draft':
            # we restrict the split of a draft move because if not confirmed yet, it may be replaced by several other moves in
            # case of phantom bom (with mrp module). And we don't want to deal with this complexity by copying the product that will explode.
            raise UserError(_('You cannot split a draft move. It needs to be confirmed first.'))
        if float_is_zero(qty, precision_rounding=self.product_id.uom_id.rounding) or self.product_qty <= qty:
            return []

        decimal_precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')

        # `qty` passed as argument is the quantity to backorder and is always expressed in the
        # quants UOM. If we're able to convert back and forth this quantity in the move's and the
        # quants UOM, the backordered move can keep the UOM of the move. Else, we'll create is in
        # the UOM of the quants.
        uom_qty = self.product_id.uom_id._compute_quantity(qty, self.product_uom, rounding_method='HALF-UP')
        if float_compare(qty, self.product_uom._compute_quantity(uom_qty, self.product_id.uom_id, rounding_method='HALF-UP'), precision_digits=decimal_precision) == 0:
            defaults = self._prepare_move_split_vals(uom_qty)
        else:
            defaults = self.with_context(force_split_uom_id=self.product_id.uom_id.id)._prepare_move_split_vals(qty)

        if restrict_partner_id:
            defaults['restrict_partner_id'] = restrict_partner_id

        # TDE CLEANME: remove context key + add as parameter
        if self.env.context.get('source_location_id'):
            defaults['location_id'] = self.env.context['source_location_id']
        new_move_vals = self.with_context(rounding_method='HALF-UP').copy_data(defaults)

        # Update the original `product_qty` of the move. Use the general product's decimal
        # precision and not the move's UOM to handle case where the `quantity_done` is not
        # compatible with the move's UOM.
        new_product_qty = self.product_id.uom_id._compute_quantity(self.product_qty - qty, self.product_uom, round=False)
        new_product_qty = float_round(new_product_qty, precision_digits=self.env['decimal.precision'].precision_get('Product Unit of Measure'))
        #self.with_context(do_not_unreserve=True, rounding_method='HALF-UP').write({'product_uom_qty': new_product_qty})
        return new_move_vals
