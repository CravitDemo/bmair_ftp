# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import xlwt
import io
import base64
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.tools import float_round


class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    @api.model
    def create(self, vals):
        res = super(MrpBom, self).create(vals)
        company_id = vals['company_id'] or self.env.company.id
        data_dict = {
            'sel_model': 'bom',
            'modification_user_id': self.env.user.id,
            'record_id': res.id,
            'trigger_function': 'create',
            'co_model_name': 'Bill OF Material',
            'record_name': res.product_tmpl_id.name,
        }

        if 'product_tmpl_id' in vals:
            data_dict.update({
                'new_value': res.product_tmpl_id.name,
                'old_value': '',
                'field_name': 'Bill of Materials / Product',
                'company_id': company_id,
            })
            self.env['bmair.history'].create(data_dict)

        if 'product_qty' in vals:
            data_dict.update({
                'new_value': res.product_qty,
                'old_value': '',
                'field_name': 'Bill of Materials / Quantity',
                'company_id': company_id,
            })
            self.env['bmair.history'].create(data_dict)

        if 'code' in vals:
            data_dict.update({
                'new_value': res.code,
                'old_value': '',
                'field_name': 'Bill of Materials / Reference',
                'company_id': company_id,
            })
            self.env['bmair.history'].create(data_dict)

        if 'type' in vals:
            if res.type == 'normal':
                bom_type_new_val = 'Manufacture this product'
            if res.type == 'phantom':
                bom_type_new_val = 'Kit'
            if res.type == 'subcontract':
                bom_type_new_val = 'Subcontracting'
            data_dict.update({
                'new_value': bom_type_new_val,
                'old_value': '',
                'field_name': 'Bill of Materials / BOM Type',
                'company_id': company_id,
            })
            self.env['bmair.history'].create(data_dict)

        if 'company_id' in vals:
            data_dict.update({
                'new_value': res.company_id.name,
                'old_value': '',
                'field_name': 'Bill of Materials / Company',
                'company_id': company_id,
            })
            self.env['bmair.history'].create(data_dict)

        return res

    def write(self, vals):
        if not self:
            res = super(MrpBom, self).write(vals)
        for mrp in self:
            product_old_val = mrp.product_tmpl_id.name
            quantity_old_val = mrp.product_qty
            reference_old_val = mrp.code
            if mrp.type == 'normal':
                bom_type_old_val = 'Manufacture this product'
            if mrp.type == 'phantom':
                bom_type_old_val = 'Kit'
            if mrp.type == 'subcontract':
                bom_type_old_val = 'Subcontracting'
            company_old_val = mrp.company_id.name

            user_id = self.env.uid
            company_id = mrp.company_id and mrp.company_id.id or self.env.company.id
            res = super(MrpBom, self).write(vals)
            data_dict = {
                    'sel_model': 'bom',
                    'record_id': mrp.id,
                    'modification_user_id': user_id,
                    'record_name': mrp.product_tmpl_id.name
                }

            if vals.get('product_tmpl_id'):
                data_dict.update({
                    'new_value': mrp.product_tmpl_id.name,
                    'old_value': product_old_val,
                    'field_name': 'Product',
                    'company_id': company_id,
                })
                self.env['bmair.history'].create(data_dict)
            if vals.get('product_qty'):
                data_dict.update({
                    'new_value': mrp.product_qty,
                    'old_value': quantity_old_val,
                    'field_name': 'Quantity',
                    'company_id': company_id,
                })
                self.env['bmair.history'].create(data_dict)
            if vals.get('code'):
                data_dict.update({
                    'new_value': mrp.code,
                    'old_value': reference_old_val,
                    'field_name': 'Reference',
                    'company_id': company_id,
                })
                self.env['bmair.history'].create(data_dict)
            if vals.get('type'):
                if mrp.type == 'normal':
                    new_value = 'Manufacture this product'
                if mrp.type == 'phantom':
                    new_value = 'Kit'
                if mrp.type == 'subcontract':
                    new_value = 'Subcontracting'
                data_dict.update({
                        'new_value': new_value,
                        'old_value': bom_type_old_val,
                        'field_name': 'BoM Type	',
                        'company_id': company_id,
                })
                self.env['bmair.history'].create(data_dict)

            if vals.get('company_id'):
                data_dict.update({
                        'new_value': mrp.company_id.name,
                        'old_value': company_old_val,
                        'field_name': 'Company',
                        'company_id': company_id,
                })
                self.env['bmair.history'].create(data_dict)

        return res

class MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'

    @api.model
    def create(self, vals):
        print("vals............cre...........",vals)
        res = super(MrpBomLine, self).create(vals)
        company_id = res.company_id and res.company_id.id or self.env.company.id
        data_dict = {
            'sel_model': 'bom',
            'modification_user_id': self.env.user.id,
            'record_id': res.bom_id.id,
            'trigger_function': 'create',
            'co_model_name': 'mrp.bom.line',
            'record_name': res.bom_id.product_tmpl_id.name
        }
        if 'product_qty' in vals:
            data_dict.update({
                'new_value': res.product_qty,
                'old_value': '',
                'field_name': 'components / Quantity',
                'company_id': company_id,
            })
            self.env['bmair.history'].create(data_dict)

        if 'product_uom_id' in vals:
            data_dict.update({
                'new_value': res.product_uom_id.name,
                'old_value': '',
                'field_name': 'components / Product Unit of measure',
                'company_id': company_id,
            })
            self.env['bmair.history'].create(data_dict)
        if 'product_id' in vals:
            data_dict.update({
                'new_value': res.product_id.product_tmpl_id.name,
                'old_value': '',
                'field_name': 'Components / Product',
                'company_id': company_id,
            })
            self.env['bmair.history'].create(data_dict)

        return res

    def write(self, vals):
        if not self:
            res = super(MrpBomLine, self).write(vals)
        for bom_line in self:
            product_qty_old_val = bom_line.product_qty
            product_uom_id_old_val = bom_line.product_uom_id.name
            product_old_val = bom_line.product_id.product_tmpl_id.name
            company_id = bom_line.company_id and bom_line.company_id.id or self.env.company.id
            res = super(MrpBomLine, self).write(vals)
            data_dict = {
                    'sel_model': 'bom',
                    'record_id': bom_line.bom_id.id,
                    'modification_user_id': bom_line.env.user.id,
                    'record_name': bom_line.bom_id.product_tmpl_id.name
                }

            if 'product_qty' in vals:
                pro_name = bom_line.product_id.product_tmpl_id.name
                data_dict.update({
                    'new_value': str(bom_line.product_qty) ,
                    'old_value': product_qty_old_val,
                    'field_name': pro_name + ' / Quantity',
                    'company_id': company_id,
                })
                self.env['bmair.history'].create(data_dict)

            if 'product_uom_id' in vals:
                pro_name = bom_line.product_id.product_tmpl_id.name
                data_dict.update({
                    'new_value': bom_line.product_uom_id.name + pro_name,
                    'old_value': product_uom_id_old_val,
                    'field_name': pro_name + ' / Product Unit of measure',
                    'company_id': company_id,
                })
                self.env['bmair.history'].create(data_dict)
            if 'product_id' in vals:
                data_dict.update({
                    'new_value': bom_line.product_id.product_tmpl_id.name ,
                    'old_value': product_old_val,
                    'field_name': 'Components / Product',
                    'company_id': company_id,
                })
                self.env['bmair.history'].create(data_dict)
        return res

    def unlink(self):
        for rec in self:
            company_id = rec.company_id and rec.company_id.id or self.env.company.id
            data_dict = {
                'sel_model': 'bom',
                'record_id': rec.bom_id.id,
                'modification_user_id': rec.env.user.id,
                'record_name': rec.bom_id.product_tmpl_id.name,
                'trigger_function' : 'delete'
            }
            if rec.product_qty:
                pro_name = rec.product_id.product_tmpl_id.name
                data_dict.update({
                    'new_value': 'False',
                    'old_value': rec.product_qty,
                    'field_name': pro_name + ' / Quantity',
                    'trigger_function': 'delete',
                    'company_id': company_id,
                })
                self.env['bmair.history'].create(data_dict)

            if rec.product_uom_id:
                pro_name = rec.product_id.product_tmpl_id.name
                data_dict.update({
                    'new_value': "False",
                    'old_value': rec.product_uom_id.name + pro_name,
                    'field_name': pro_name + ' / Product Unit of measure',
                    'trigger_function': 'delete',
                    'company_id': company_id,
                })
                self.env['bmair.history'].create(data_dict)

            if rec.product_id:
                pro_name = rec.product_id.product_tmpl_id.name
                data_dict.update({
                    'new_value': "False",
                    'old_value': rec.product_id.product_tmpl_id.name,
                    'field_name': pro_name + ' / Product',
                    'trigger_function': 'delete',
                    'company_id': company_id,
                })
                self.env['bmair.history'].create(data_dict)

        res = super(MrpBomLine, self).unlink()
        print("res................",res)
        return res

class MrpRoutingWorkcenter(models.Model):
    _inherit = 'mrp.routing.workcenter'

    @api.model
    def create(self, vals):
        res = super(MrpRoutingWorkcenter, self).create(vals)
        company_id = vals['company_id']
        data_dict = {
            'sel_model': 'bom',
            'modification_user_id': self.env.user.id,
            'record_id': res.bom_id.id,
            'trigger_function': 'create',
            'co_model_name': 'mrp.routing.workcenter',
            'record_name': res.bom_id.product_tmpl_id.name
        }

        if 'name' in vals:
            data_dict.update({
                'new_value': res.name,
                'old_value': '',
                'field_name': 'Operations / Operation',
                'company_id': company_id,
            })
            self.env['bmair.history'].create(data_dict)

        if 'workcenter_id' in vals:
            data_dict.update({
                'new_value': res.workcenter_id.name,
                'old_value': '',
                'field_name': 'Operations / Work Center',
                'company_id': company_id,
            })
            self.env['bmair.history'].create(data_dict)

        if 'time_cycle_manual' in vals:
            data_dict.update({
                'new_value': res.time_cycle_manual,
                'old_value': '',
                'field_name': 'Operations / Duration (minutes)',
                'company_id': company_id,
            })
            self.env['bmair.history'].create(data_dict)

        return res

    def write(self, vals):
        name_old_val = self.name
        time_cycle_manual_old_val = self.time_cycle_manual
        workcenter_id_old_val = self.workcenter_id.name

        res = super(MrpRoutingWorkcenter, self).write(vals)
        data_dict = {
                'sel_model': 'bom',
                'record_id': self.bom_id.id,
                'modification_user_id': self.env.user.id,
                'record_name': self.bom_id.product_tmpl_id.name
            }

        if 'name' in vals:
            data_dict.update({
                'new_value': self.name,
                'old_value': name_old_val,
                'field_name': 'Operations / Operation',
            })
            self.env['bmair.history'].create(data_dict)

        if 'time_cycle_manual' in vals:
            data_dict.update({
                'new_value': self.time_cycle_manual,
                'old_value': time_cycle_manual_old_val,
                'field_name': 'Operations / Duration (minutes)',
            })
            self.env['bmair.history'].create(data_dict)

        if 'workcenter_id' in vals:
            data_dict.update({
                'new_value': self.workcenter_id.name,
                'old_value': workcenter_id_old_val,
                'field_name': 'Operations / Work Center',
            })
            self.env['bmair.history'].create(data_dict)
        return res
