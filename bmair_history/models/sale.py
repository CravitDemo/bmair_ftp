# -*- coding: utf-8 -*-


from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def write(self, values):
        rec = True
        for sale in self:
            pricelist_val = sale.pricelist_id.name
            payment_term_val = sale.payment_term_id.name
            commitment_date_val = sale.commitment_date
            fiscal_position_val = self.fiscal_position_id.name
            user_id = self.env.uid
            company_id = sale.company_id and sale.company_id.id or self.env.company.id

            if values.get('order_line'):
                dic = {}
                for line in values['order_line']:
                    if type(line[1]) == int:
                        if line[2] != False:
                            line_id = line[1]
                            if line[2].get('price_unit') or line[2].get('price_unit') == 0.0:
                                price_unit = self.env['sale.order.line'].search([('id', '=', line[1])]).price_unit
                                dic[line_id] = {'price_unit' : price_unit}
                            if line[2].get('discount') or line[2].get('discount') == 0.0:
                                discount = self.env['sale.order.line'].search([('id', '=', line[1])]).discount
                                if line[1] in list(dic.keys()):
                                    dic[line_id].update({'discount': discount})
                                else:
                                    dic[line_id] = {'discount': discount}

            rec = super(SaleOrder, self).write(values)
            com_vals = {
                'sel_model': 'sale_order',
                'record_id': str(sale.id),
                'modification_user_id': user_id,
                'record_name': sale.name
            }
            if values.get('pricelist_id') or values.get('pricelist_id') == False:
                pricelist_vals = {
                    'old_value': pricelist_val,
                    'new_value':  sale.pricelist_id.name,
                    'field_name': 'Pricelist',
                    'company_id': company_id,
                }
                pricelist_vals.update(com_vals)
                self.env['bmair.history'].create(pricelist_vals)

            if values.get('payment_term_id') or values.get('payment_term_id') == False:
                payment_terms_vals = {
                    'old_value': payment_term_val,
                    'new_value': sale.payment_term_id.name,
                    'field_name': 'Payment Terms',
                    'company_id': company_id,
                }
                payment_terms_vals.update(com_vals)
                self.env['bmair.history'].create(payment_terms_vals)

            if values.get('commitment_date') or values.get('commitment_date') == False:
                delivery_date_vals = {
                    'old_value': commitment_date_val,
                    'new_value': sale.commitment_date,
                    'field_name': 'Delivery Date',
                    'company_id': company_id,
                }
                delivery_date_vals.update(com_vals)
                self.env['bmair.history'].create(delivery_date_vals)

            if values.get('fiscal_position_id') or values.get('fiscal_position_id') == False:
                fiscal_position_vals = {
                    'old_value': fiscal_position_val,
                    'new_value': sale.fiscal_position_id.name,
                    'field_name': 'Fiscal Position',
                    'company_id': company_id,
                }
                fiscal_position_vals.update(com_vals)
                self.env['bmair.history'].create(fiscal_position_vals)

            if values.get('order_line'):
                for line in values['order_line']:
                    if line[2] != False and (line[2].get('price_unit') or line[2].get('price_unit') == 0.0):
                        if type(line[1]) == int:
                            price_unit_vals = {
                                'old_value': dic[line[1]].get('price_unit'),
                                'new_value': line[2]['price_unit'],
                                'field_name': 'Order lines / Unit Price',
                                'company_id': company_id,
                            }
                            price_unit_vals.update(com_vals)
                            self.env['bmair.history'].create(price_unit_vals)
                        else:
                            price_unit_vals = {
                                'old_value': '',
                                'new_value': line[2]['price_unit'],
                                'field_name': 'Order lines / Unit Price',
                                'company_id': company_id,
                            }
                            if price_unit_vals['new_value'] != 0.0:
                                price_unit_vals.update(com_vals)
                                self.env['bmair.history'].create(price_unit_vals)
                    if line[2] != False and (line[2].get('discount') or line[2].get('discount') == 0.0):
                        if type(line[1]) == int:
                            discount_vals = {
                                'old_value': dic[line[1]].get('discount'),
                                'new_value': line[2]['discount'],
                                'field_name': 'Order lines / Disc%',
                                'company_id': company_id,
                            }
                            discount_vals.update(com_vals)
                            self.env['bmair.history'].create(discount_vals)
                        else:
                            discount_vals = {
                                'old_value': '',
                                'new_value': line[2]['discount'],
                                'field_name': 'Order lines / Disc%',
                                'company_id': company_id,
                            }
                            if discount_vals['new_value'] != 0.0:
                                discount_vals.update(com_vals)
                                self.env['bmair.history'].create(discount_vals)

        return rec
