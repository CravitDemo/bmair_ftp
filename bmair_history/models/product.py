# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models
import re
import json


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def write(self, vals):
        if not self:
            res = super(ProductTemplate, self).write(vals)
        for product in self:

            name_old_val = self.name
            if not product.sale_ok:
                sale_ok_old_val = 'False'
            else:
                sale_ok_old_val = 'True'
            if not product.purchase_ok:
                purchase_ok_old_val = 'False'
            else:
                purchase_ok_old_val = 'True'

            if not product.can_be_expensed:
                can_be_expensed_old_val = 'False'
            else:
                can_be_expensed_old_val = 'True'

            if 'type' in vals:
                if product.type == 'consu':
                    type_old_val = 'Consumable'
                if product.type == 'service':
                    type_old_val = 'Service'
                if product.type == 'product':
                    type_old_val = 'Storable Product'

            categ_id_old_val = product.categ_id.display_name
            default_code_old_val = product.default_code
            barcode_old_val = product.barcode
            list_price_old_val = product.list_price
            standard_price_old_val = product.standard_price
            uom_id_old_val = product.uom_id.name
            uom_po_id_old_val = product.uom_po_id.name
            if product.invoice_policy == 'order':
                invoice_policy_old_val = 'Ordered Quantities'
            if product.invoice_policy == 'delivery':
                invoice_policy_old_val = 'Delivered Quantities'
            description_sale_old_val = product.description_sale
            sale_line_warn_msg_old_val = product.sale_line_warn_msg
            sale_line_warn_old_val = product.sale_line_warn
            description_purchase_old_val = product.description_purchase
            route_ids_old_val = ''
            company_id = product.company_id and product.company_id.id or self.env.company.id
            if 'route_ids' in vals:
                for old_rt in product.route_ids:
                    if route_ids_old_val:
                        route_ids_get = ' , ' + str(old_rt.name)
                        route_ids_old_val += route_ids_get
                    else:
                        route_ids_old_val = str(old_rt.name)

            if 'tracking' in vals:
                if product.tracking == 'serial':
                    tracking_old_val = 'By Unique Serial Number'
                if product.tracking == 'lot':
                    tracking_old_val = 'By Lots'
                if product.tracking == 'none':
                    tracking_old_val = 'No Tracking'

            description_pickingout_old_val = product.description_pickingout
            produce_delay_old_val = product.produce_delay
            sale_delay_old_val = product.sale_delay
            company_id_old_val = product.company_id.name
            taxes_id_old_val = ''
            if 'taxes_id' in vals:
                for tx in product.taxes_id:
                    if taxes_id_old_val:
                        tx_name = ' , ' + tx.name
                        taxes_id_old_val += tx_name
                    else:
                        taxes_id_old_val = tx.name

            res = super(ProductTemplate, self).write(vals)
            data_dict = {
                'sel_model': 'product',
                'modification_user_id': self.env.user.id,
                'record_id': str(product.id),
                'record_name': product.name,
            }
            if 'name' in vals:
                data_dict.update({
                    'field_name': 'Name',
                    'old_value': name_old_val,
                    'new_value': self.name,
                    'company_id': company_id,

                })
                self.env['bmair.history'].create(data_dict)

            if 'sale_ok' in vals:
                if not product.sale_ok:
                    new_sale_ok = 'False'
                if product.sale_ok:
                    new_sale_ok = 'True'
                data_dict.update({
                    'field_name': 'Can be Sold',
                    'old_value': sale_ok_old_val,
                    'new_value': new_sale_ok,
                    'company_id': company_id,
                })
                self.env['bmair.history'].create(data_dict)

            if 'purchase_ok' in vals:
                if not product.purchase_ok:
                    new_purchase_ok = 'False'
                if product.purchase_ok:
                    new_purchase_ok = 'True'
                data_dict.update({
                    'field_name': 'Can be Purchased',
                    'old_value': purchase_ok_old_val,
                    'new_value': new_purchase_ok,
                    'company_id': company_id,
                })
                self.env['bmair.history'].create(data_dict)

            if 'can_be_expensed' in vals:
                if not product.can_be_expensed:
                    new_can_be_expensed = 'False'
                if product.can_be_expensed:
                    new_can_be_expensed = 'True'
                data_dict.update({
                    'field_name': 'Can be Expensed',
                    'old_value': can_be_expensed_old_val,
                    'new_value': new_can_be_expensed,
                    'company_id': company_id,
                })
                self.env['bmair.history'].create(data_dict)

            if 'type' in vals:
                if product.type == 'consu':
                    type_new_val = 'Consumable'
                if product.type == 'service':
                    type_new_val = 'Service'
                if product.type == 'product':
                    type_new_val = 'Storable Product'
                data_dict.update({
                    'field_name': 'Product Type',
                    'old_value': type_old_val,
                    'new_value': type_new_val,
                    'company_id': company_id,
                })
                self.env['bmair.history'].create(data_dict)

            if 'categ_id' in vals:
                data_dict.update({
                    'field_name': 'Product Category',
                    'old_value': categ_id_old_val,
                    'new_value': product.categ_id.display_name,
                    'company_id': company_id,
                })
                self.env['bmair.history'].create(data_dict)

            if 'default_code' in vals:
                data_dict.update({
                    'field_name': 'Internal Reference',
                    'old_value': default_code_old_val,
                    'new_value': product.default_code,
                    'company_id': company_id,
                })
                self.env['bmair.history'].create(data_dict)

            if 'barcode' in vals:
                data_dict.update({
                    'field_name': 'Barcode',
                    'old_value': barcode_old_val,
                    'new_value': product.barcode,
                    'company_id': company_id,
                })
                self.env['bmair.history'].create(data_dict)

            if 'list_price' in vals:
                data_dict.update({
                    'field_name': 'Sales Price',
                    'old_value': list_price_old_val,
                    'new_value': product.list_price,
                    'company_id': company_id,
                })
                self.env['bmair.history'].create(data_dict)

            if 'standard_price' in vals:
                data_dict.update({
                    'field_name': 'Cost',
                    'old_value': standard_price_old_val,
                    'new_value': product.standard_price,
                    'company_id': company_id,
                })
                self.env['bmair.history'].create(data_dict)

            if 'uom_id' in vals:
                data_dict.update({
                    'field_name': 'Unit of Measure',
                    'old_value': uom_id_old_val,
                    'new_value': product.uom_id.name,
                    'company_id': company_id,
                })
                self.env['bmair.history'].create(data_dict)

            if 'uom_po_id' in vals:
                data_dict.update({
                    'field_name': 'Purchase Unit of Measure',
                    'old_value': uom_po_id_old_val,
                    'new_value': product.uom_po_id.name,
                    'company_id': company_id,
                })
                self.env['bmair.history'].create(data_dict)

            if 'invoice_policy' in vals:
                if product.invoice_policy == 'order':
                    invoice_policy_new_val = 'Ordered Quantities'
                if product.invoice_policy == 'delivery':
                    invoice_policy_new_val = 'Delivered Quantities'
                data_dict.update({
                    'field_name': 'Invoicing Policy',
                    'old_value': invoice_policy_old_val,
                    'new_value': invoice_policy_new_val,
                    'company_id': company_id,
                })
                self.env['bmair.history'].create(data_dict)

            if 'description_sale' in vals:
                data_dict.update({
                    'field_name': 'Sales Description',
                    'old_value': description_sale_old_val,
                    'new_value': product.description_sale,
                    'company_id': company_id,
                })
                self.env['bmair.history'].create(data_dict)

            if 'sale_line_warn_msg' in vals:
                data_dict.update({
                    'field_name': 'Warning when Selling this Product Message',
                    'old_value': sale_line_warn_msg_old_val,
                    'new_value': product.sale_line_warn_msg,
                    'company_id': company_id,
                })
                self.env['bmair.history'].create(data_dict)

            if 'sale_line_warn' in vals:
                data_dict.update({
                    'field_name': 'Warning when Selling this Product',
                    'old_value': sale_line_warn_old_val,
                    'new_value': product.sale_line_warn,
                    'company_id': company_id,
                })
                self.env['bmair.history'].create(data_dict)

            if 'seller_ids' in vals:
                for seller in vals.get('seller_ids'):
                    if seller and seller[2]:
                        if 'name' in seller[2]:
                            slr_id = seller[2].get('name')
                            get_partner = self.env['res.partner'].browse(slr_id)
                            if get_partner:
                                data_dict.update({
                                    'field_name': 'Seller',
                                    'old_value': '',
                                    'new_value': get_partner.name,
                                    'company_id': company_id,
                                })
                                if type(seller[1]) != int:
                                    self.env['bmair.history'].create(data_dict)

                        if 'product_code' in seller[2] and seller[2].get('product_code') != False:
                            data_dict.update({
                                'field_name': 'Seller / Product Code',
                                'old_value': '',
                                'new_value': seller[2].get('product_code'),
                                'company_id': company_id,
                            })
                            if type(seller[1]) != int:
                                self.env['bmair.history'].create(data_dict)

                        if 'price' in seller[2] and seller[2].get('price') != 0:
                            data_dict.update({
                                'field_name': 'Seller / Price',
                                'old_value': '',
                                'new_value': seller[2].get('price'),
                                'company_id': company_id,
                            })
                            if type(seller[1]) != int:
                                self.env['bmair.history'].create(data_dict)

                        if 'delay' in seller[2]:
                            data_dict.update({
                                'field_name': 'Seller / Delivery Lead time',
                                'old_value': '',
                                'new_value': seller[2].get('delay'),
                                'company_id': company_id,
                            })
                            if type(seller[1]) != int:
                                self.env['bmair.history'].create(data_dict)

            if 'description_purchase' in vals:
                data_dict.update({
                    'field_name': 'Purchase Description',
                    'old_value': description_purchase_old_val,
                    'new_value': product.description_purchase,
                    'company_id': company_id,
                })
                self.env['bmair.history'].create(data_dict)

            route_ids_new_val = ''
            if 'route_ids' in vals:
                for new_rt in product.route_ids:
                    if route_ids_new_val:
                        route_ids_get = ' , ' + str(new_rt.name)
                        route_ids_new_val += route_ids_get
                    else:
                        route_ids_new_val = str(new_rt.name)

                data_dict.update({
                    'field_name': 'Routes',
                    'old_value': route_ids_old_val,
                    'new_value': route_ids_new_val,
                    'company_id': company_id,
                })
                self.env['bmair.history'].create(data_dict)

            if 'tracking' in vals:
                if product.tracking == 'serial':
                    tracking_new_val = 'By Unique Serial Number'
                if product.tracking == 'lot':
                    tracking_new_val = 'By Lots'
                if product.tracking == 'none':
                    tracking_new_val = 'No Tracking'

                data_dict.update({
                    'field_name': 'Tracking',
                    'old_value': tracking_old_val,
                    'new_value': tracking_new_val,
                    'company_id': company_id,
                })
                self.env['bmair.history'].create(data_dict)

            if 'description_pickingout' in vals:
                data_dict.update({
                    'field_name': 'Description for Delivery Orders',
                    'old_value': description_pickingout_old_val,
                    'new_value': product.description_pickingout,
                    'company_id': company_id,
                })
                self.env['bmair.history'].create(data_dict)

            if 'produce_delay' in vals:
                data_dict.update({
                    'field_name': 'Manufacturing Lead Time',
                    'old_value': produce_delay_old_val,
                    'new_value': product.produce_delay,
                    'company_id': company_id,
                })
                self.env['bmair.history'].create(data_dict)

            if 'sale_delay' in vals:
                data_dict.update({
                    'field_name': 'Customer lead time',
                    'old_value': sale_delay_old_val,
                    'new_value': product.sale_delay,
                    'company_id': company_id,
                })
                self.env['bmair.history'].create(data_dict)

            if 'company_id' in vals:
                data_dict.update({
                    'field_name': 'Company',
                    'old_value': company_id_old_val,
                    'new_value': product.company_id.name,
                    'company_id': company_id,
                })
                self.env['bmair.history'].create(data_dict)

            taxes_id_new_val = ''
            if 'taxes_id' in vals:
                for tx in product.taxes_id:
                    if taxes_id_new_val:
                        tx_name = ' , ' + tx.name
                        taxes_id_new_val += tx_name
                    else:
                        taxes_id_new_val = tx.name
                data_dict.update({
                    'field_name': 'Customer Taxes',
                    'old_value': taxes_id_old_val,
                    'new_value': taxes_id_new_val,
                    'company_id': company_id,
                })
                self.env['bmair.history'].create(data_dict)

        return res


class ProductSuppInfo(models.Model):
    _inherit = 'product.supplierinfo'

    def write(self, vals):
        if not self:
            res = super(ProductSuppInfo, self).write(vals)
        for supp in self:
            name_old_val = supp.name.commercial_partner_id.name
            product_code_old_val = supp.product_code
            price_old_val = supp.price
            delay_old_val = supp.delay
            sequence_old_val = supp.sequence
            company_id = supp.company_id and supp.company_id.id or self.env.company.id
            res = super(ProductSuppInfo, self).write(vals)
            data_dict = {
                'sel_model': 'product',
                'modification_user_id': self.env.user.id,
                'record_id': str(supp.product_tmpl_id.id),
                'record_name': supp.product_tmpl_id.name
            }
            if 'name' in vals:
                slr_id = vals.get('name')
                get_partner = self.env['res.partner'].browse(slr_id)
                data_dict.update({
                    'field_name': 'Seller',
                    'old_value': name_old_val,
                    'new_value': supp.name.commercial_partner_id.name,
                    'company_id': company_id,
                })
                self.env['bmair.history'].create(data_dict)

            if 'product_code' in vals:
                data_dict.update({
                    'field_name': 'Seller / Product Code',
                    'old_value': product_code_old_val,
                    'new_value': supp.product_code,
                    'company_id': company_id,
                })
                self.env['bmair.history'].create(data_dict)

            if 'price' in vals:
                data_dict.update({
                    'field_name': 'Seller / Price',
                    'old_value': price_old_val,
                    'new_value': supp.price,
                    'company_id': company_id,
                })
                self.env['bmair.history'].create(data_dict)

            if 'delay' in vals:
                data_dict.update({
                    'field_name': 'Seller / Delay',
                    'old_value': delay_old_val,
                    'new_value': supp.delay,
                    'company_id': company_id,
                })
                self.env['bmair.history'].create(data_dict)
            if 'sequence' in vals:
                data_dict.update({
                    'field_name': 'Seller / Sequence',
                    'old_value': sequence_old_val,
                    'new_value': supp.sequence,
                    'company_id': company_id,
                })
                self.env['bmair.history'].create(data_dict)

        return res

    def unlink(self):
        for rec in self:
            company_id = rec.company_id and rec.company_id.id or self.env.company.id
            data_dict = {
                'sel_model': 'product',
                'record_id': rec.product_tmpl_id.id,
                'modification_user_id': rec.env.user.id,
                'record_name': rec.product_tmpl_id.name,
                'trigger_function': 'delete',
            }
            if rec.name:
                p_name = rec.name.name
                if not rec.name.name and rec.name.parent_id and rec.name.parent_id.name:
                    p_name = rec.name.parent_id.name
                data_dict.update({
                    'new_value': 'False',
                    'old_value': p_name,
                    'field_name': 'Product / Supplier',
                    'trigger_function': 'delete',
                    'company_id': company_id,
                })
                self.env['bmair.history'].create(data_dict)

        res = super(ProductSuppInfo, self).unlink()
        return res


class StockWarehouseOrderpoint(models.Model):
    _inherit = 'stock.warehouse.orderpoint'

    @api.model
    def create(self, vals):
        res = super(StockWarehouseOrderpoint, self).create(vals)
        company_id = res.company_id and res.company_id.id or self.env.company.id
        data_dict = {
            'sel_model': 'product',
            'modification_user_id': self.env.user.id,
            'record_id': str(res.product_tmpl_id.id),
            'trigger_function': 'create',
            'co_model_name': 'Re-Ordering rule',
            'record_name': res.product_tmpl_id.name
        }
        if 'location_id' in vals:
            data_dict.update({
                'field_name': 'Location',
                'old_value': '',
                'new_value': res.location_id.complete_name,
                'company_id': company_id,
            })
            self.env['bmair.history'].create(data_dict)

        if 'product_min_qty' in vals:
            data_dict.update({
                'field_name': 'Re-Ordering rule / Min Quantity',
                'old_value': '',
                'new_value': res.product_min_qty,
                'company_id': company_id,
            })
            self.env['bmair.history'].create(data_dict)

        if 'product_max_qty' in vals:
            data_dict.update({
                'field_name': 'Re-Ordering rule / Max Quantity',
                'old_value': '',
                'new_value': res.product_max_qty,
                'company_id': company_id,
            })
            self.env['bmair.history'].create(data_dict)

        if 'qty_multiple' in vals:
            data_dict.update({
                'field_name': 'Re-Ordering rule / Quantity Multiple',
                'old_value': '',
                'new_value': res.qty_multiple,
                'company_id': company_id,
            })
            self.env['bmair.history'].create(data_dict)
        return res

    def write(self, vals):
        if not self:
            res = super(StockWarehouseOrderpoint, self).write(vals)
        for re_rule in self:
            location_id_old_val = re_rule.location_id.complete_name
            product_min_qty_old_val = re_rule.product_min_qty
            product_max_qty_old_val = re_rule.product_max_qty
            qty_multiple_old_val = re_rule.qty_multiple
            company_id = re_rule.company_id and re_rule.company_id.id or self.env.company.id

            res = super(StockWarehouseOrderpoint, self).write(vals)
            data_dict = {
                'sel_model': 'product',
                'modification_user_id': self.env.user.id,
                'record_id': str(re_rule.product_tmpl_id.id),
                'record_name': re_rule.product_tmpl_id.name
            }
            if 'location_id' in vals:
                data_dict.update({
                    'field_name': 'Re-Ordering rule / Location',
                    'old_value': location_id_old_val,
                    'new_value': re_rule.location_id.complete_name,
                    'company_id': company_id,
                })
                self.env['bmair.history'].create(data_dict)

            if 'product_min_qty' in vals:
                data_dict.update({
                    'field_name': 'Re-Ordering rule / Min Quantity',
                    'old_value': product_min_qty_old_val,
                    'new_value': re_rule.product_min_qty,
                    'company_id': company_id,
                })
                self.env['bmair.history'].create(data_dict)

            if 'product_max_qty' in vals:
                data_dict.update({
                    'field_name': 'Re-Ordering rule / Max Quantity',
                    'old_value': product_max_qty_old_val,
                    'new_value': re_rule.product_max_qty,
                    'company_id': company_id,
                })
                self.env['bmair.history'].create(data_dict)

            if 'qty_multiple' in vals:
                data_dict.update({
                    'field_name': 'Re-Ordering rule / Quantity Multiple',
                    'old_value': qty_multiple_old_val,
                    'new_value': re_rule.qty_multiple,
                    'company_id': company_id,
                })
                self.env['bmair.history'].create(data_dict)
        return res


class StockPutawayRule(models.Model):
    _inherit = 'stock.putaway.rule'

    @api.model
    def create(self, vals):
        res = super(StockPutawayRule, self).create(vals)
        company_id = vals['company_id']
        data_dict = {
            'sel_model': 'product',
            'modification_user_id': self.env.user.id,
            'record_id': str(res.product_id.product_tmpl_id.id),
            'trigger_function': 'create',
            'co_model_name': 'Putaway rules',
            'record_name': res.product_id.product_tmpl_id.name
        }

        if 'product_id' in vals:
            data_dict.update({
                'field_name': 'Putaway rules / Product',
                'old_value': '',
                'new_value': res.product_id.product_tmpl_id.name,
                'company_id': company_id,
            })
            self.env['bmair.history'].create(data_dict)

        if 'location_in_id' in vals:
            data_dict.update({
                'field_name': 'Putaway rules / When product arrives in',
                'old_value': '',
                'new_value': res.location_in_id.complete_name,
                'company_id': company_id,
            })
            self.env['bmair.history'].create(data_dict)

        if 'location_out_id' in vals:
            data_dict.update({
                'field_name': 'Putaway rules / Store to',
                'old_value': '',
                'new_value': res.location_out_id.complete_name,
                'company_id': company_id,
            })
            self.env['bmair.history'].create(data_dict)

        if 'company_id' in vals:
            data_dict.update({
                'field_name': 'Putaway rules / Company',
                'old_value': '',
                'new_value': res.company_id.name,
                'company_id': company_id,
            })
            self.env['bmair.history'].create(data_dict)

        return res

    def write(self, vals):
        if not self:
            res = super(StockPutawayRule, self).write(vals)
        for put_away in self:
            location_in_id_old_val = put_away.location_in_id.complete_name
            location_out_id_old_val = put_away.location_out_id.complete_name
            company_id_old_val = put_away.company_id
            company_id = put_away.company_id and put_away.company_id.id or self.env.company.id

            res = super(StockPutawayRule, self).write(vals)
            data_dict = {
                'sel_model': 'product',
                'modification_user_id': self.env.user.id,
                'record_id': str(put_away.product_id.product_tmpl_id.id),
                'record_name': put_away.product_id.product_tmpl_id.name
            }

            if 'location_in_id' in vals:
                data_dict.update({
                    'field_name': 'Putaway rules / When product arrives in',
                    'old_value': location_in_id_old_val,
                    'new_value': put_away.location_in_id.complete_name,
                    'company_id': company_id,
                })
                self.env['bmair.history'].create(data_dict)

            if 'location_out_id' in vals:
                data_dict.update({
                    'field_name': 'Putaway rules / Store to',
                    'old_value': location_out_id_old_val,
                    'new_value': put_away.location_out_id.complete_name,
                    'company_id': company_id,
                })
                self.env['bmair.history'].create(data_dict)

            if 'company_id' in vals:
                data_dict.update({
                    'field_name': 'Putaway rules / Company',
                    'old_value': company_id_old_val,
                    'new_value': put_away.company_id.name,
                    'company_id': company_id,
                })
                self.env['bmair.history'].create(data_dict)

        return res
