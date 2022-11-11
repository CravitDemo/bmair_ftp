# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models
from odoo.exceptions import UserError,ValidationError
from re import findall as regex_findall
from re import split as regex_split


class MrpAssignSerialNumbers(models.TransientModel):
    _name = 'mrp.assign.serial'
    _description = 'MRP Assign Serial Numbers'

    def _default_next_serial_count(self):
        mo = self.env['mrp.production'].browse(self.env.context.get('default_mo_id'))
        if mo.exists():
            return mo.product_uom_qty

    product_id = fields.Many2one('product.product', 'Product', related='mo_id.product_id', required=True)
    mo_id = fields.Many2one('mrp.production', required=True)
    prefix_char = fields.Char('First SN')
    next_serial_count = fields.Integer('Number of SN', default=_default_next_serial_count, readonly=True)

    @api.constrains('next_serial_count')
    def _check_next_serial_count(self):
        for wizard in self:
            if wizard.next_serial_count < 1:
                raise ValidationError(_("The number of Serial Numbers to generate must greater than zero."))

    def _generate_serial_numbers(self, next_serial_count=False):
        """ This method will generate `lot_name` from a string (field
        `next_serial`) and create a move line for each generated `lot_name`.
        """
        self.ensure_one()

        if not next_serial_count:
            next_serial_count = self.next_serial_count
        caught_initial_number = regex_findall("\d+", self.prefix_char)
        if not caught_initial_number:
            raise UserError(_('The serial number must contain at least one digit.'))
        initial_number = caught_initial_number[-1]
        padding = len(initial_number)
        splitted = regex_split(initial_number, self.prefix_char)
        prefix = initial_number.join(splitted[:-1])
        suffix = splitted[-1]
        initial_number = int(initial_number)

        lot_names = []
        for i in range(0, next_serial_count):
            lot_names.append('%s%s%s' % (
                prefix,
                str(initial_number + i).zfill(padding),
                suffix
            ))
        #move_lines_commands = self._generate_serial_move_line_commands(lot_names)
        #self.mo_id.write({'move_line_ids': move_lines_commands})
        return lot_names

    def generate_serial_numbers(self):
        # Assign serial number based on default function
        self.ensure_one()
        '''if self.mo_id.state != 'confirmed' and self.mo_id.state == 'draft':
            raise UserError(_('You cannot generate lot/serial number for draft MO'))  '''          
        serials = self._generate_serial_numbers(next_serial_count=self.next_serial_count)
        self.mo_id.lot_producing_id = self.env['stock.production.lot'].create({
            'name' : serials[0],
            'product_id': self.mo_id.product_id.id,
            'company_id': self.mo_id.company_id.id,
        })
        if self.mo_id.move_finished_ids.filtered(lambda m: m.product_id == self.mo_id.product_id).move_line_ids:
            self.mo_id.move_finished_ids.filtered(lambda m: m.product_id == self.mo_id.product_id).move_line_ids.lot_id = self.mo_id.lot_producing_id
        if self.mo_id.product_id.tracking == 'serial':
            self.mo_id._set_qty_producing()
        mo_id = self.mo_id
        a = 1
        mo_list = [self.mo_id]
        while self.next_serial_count >=1 and mo_id.product_uom_qty > 1:
            bo_id = mo_id._generate_backorder_productions(close_mo=False)
            bo_id.lot_producing_id = self.env['stock.production.lot'].create({
                'name' : serials[a],
                'product_id': self.mo_id.product_id.id,
                'company_id': self.mo_id.company_id.id,
                })
            if self.mo_id.move_finished_ids.filtered(lambda m: m.product_id == self.mo_id.product_id).move_line_ids:
                self.mo_id.move_finished_ids.filtered(lambda m: m.product_id == self.mo_id.product_id).move_line_ids.lot_id = self.mo_id.lot_producing_id
            if self.mo_id.product_id.tracking == 'serial':
                self.mo_id._set_qty_producing()

            # for next backorder generate
            mo_id = bo_id
            mo_list.append(bo_id)

            a = a+1
        # for blocking resplitting 
        for mo in mo_list:
            mo.write({'product_qty':1,'product_uom_qty':1})
        
            self.mo_id.write({'product_qty':1, 'product_uom_qty':1})
            if mo.bom_id and mo.product_qty > 0:
                # keep manual entries
                list_move_raw = [(4, move.id) for move in mo.move_raw_ids.filtered(lambda m: not m.bom_line_id)]
                moves_raw_values = mo._get_moves_raw_values()
                move_raw_dict = {move.bom_line_id.id: move for move in mo.move_raw_ids.filtered(lambda m: m.bom_line_id)}
                for move_raw_values in moves_raw_values:
                    move_raw_values.pop('state')
                    if move_raw_values['bom_line_id'] in move_raw_dict:
                        # update existing entries
                        list_move_raw += [(1, move_raw_dict[move_raw_values['bom_line_id']].id, move_raw_values)]
                    else:
                        # add new entries
                        list_move_raw += [(0, 0, move_raw_values)]
                mo.move_raw_ids = list_move_raw
            else:
                mo.move_raw_ids = [(2, move.id) for move in self.mo_id.move_raw_ids.filtered(lambda m: m.bom_line_id)]
            mo.action_assign()

