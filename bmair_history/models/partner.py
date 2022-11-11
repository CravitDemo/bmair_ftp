# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models
import re
import json


class Partner(models.Model):
    _inherit = 'res.partner'

    def write(self, vals):
        if not self:
            res = super(Partner, self).write(vals)
        for partner in self:
            sale_warn_old_val = partner.sale_warn
            sale_warn_msg_old_val = partner.sale_warn_msg
            invoice_warn_old_val = partner.invoice_warn
            invoice_warn_msg_old_val = partner.invoice_warn_msg
            check_credit_old_val = partner.check_credit
            if not partner.check_credit:
                check_credit_old_val = 'False'
            if 'bank_ids' in vals:
                bank_ids_old_val = ''
                for bank_id in partner.bank_ids:
                    if bank_ids_old_val:
                        new_val_bank = ' , ' + '[' + bank_id.bank_id.name + ' : ' + str(bank_id.acc_number) + ']'
                        bank_ids_old_val += new_val_bank
                    else:
                        bank_ids_old_val = '[' + bank_id.bank_id.name + ' : ' + str(bank_id.acc_number) + ']'

            credit_limit_old_val = partner.credit_limit
            property_payment_term_id_old_val = partner.property_payment_term_id
            property_supplier_payment_term_id_old_val = partner.property_supplier_payment_term_id
            property_product_pricelist_id_old_val = partner.property_product_pricelist
            property_account_position_id_old_val = partner.property_account_position_id
            vat_old_val = partner.vat
            company_id = partner.company_id and partner.company_id.id or self.env.company.id

            res = super(Partner, self).write(vals)
            data_dict = {
                'sel_model': 'contact',
                'modification_user_id': partner.env.user.id,
                'record_id': str(partner.id),
                'record_name': partner.commercial_partner_id.name
            }
            if 'bank_ids' in vals:
                bank_ids_new_val = ''
                for bank_id in partner.bank_ids:
                    if bank_ids_new_val:
                        new_val_bank = ' , ' + '[' + bank_id.bank_id.name + ' : ' + str(bank_id.acc_number) + ']'
                        bank_ids_new_val += new_val_bank
                    else:
                        bank_ids_new_val = '[' + bank_id.bank_id.name + ' : ' + str(bank_id.acc_number) + ']'

                bank_data = {
                    'sel_model': 'contact',
                    'modification_user_id': self.env.user.id,
                    'record_id': str(partner.id),
                    'old_value': bank_ids_old_val,
                    'new_value': bank_ids_new_val,
                    'field_name': 'Contact / Bank Account',
                    'record_name': partner.commercial_partner_id.name,
                    'company_id': company_id,
                }
                self.env['bmair.history'].create(bank_data)

            if 'check_credit' in vals:
                check_credit = "True"
                if not partner.check_credit:
                    check_credit = 'False'
                data_dict.update({
                    'field_name': 'Check Credit',
                    'old_value': check_credit_old_val,
                    'new_value': check_credit,
                    'company_id': company_id,
                })
                self.env['bmair.history'].create(data_dict)

            if 'sale_warn' in vals:
                data_dict.update({
                    'field_name': 'Warning on the sales order',
                    'old_value': sale_warn_old_val,
                    'new_value': partner.sale_warn,
                    'company_id': company_id,
                })
                self.env['bmair.history'].create(data_dict)

            if 'sale_warn_msg' in vals:
                data_dict.update({
                    'field_name': 'Warning on the sales order Message',
                    'old_value': sale_warn_msg_old_val,
                    'new_value': partner.sale_warn_msg,
                    'company_id': company_id,
                })
                self.env['bmair.history'].create(data_dict)

            if 'invoice_warn' in vals:
                data_dict.update({
                    'field_name': 'Warning on the invoice',
                    'old_value': invoice_warn_old_val,
                    'new_value': partner.invoice_warn,
                    'company_id': company_id,
                })
                self.env['bmair.history'].create(data_dict)

            if 'invoice_warn_msg' in vals:
                data_dict.update({
                    'field_name': 'Warning on the invoice Message',
                    'old_value': invoice_warn_msg_old_val,
                    'new_value': partner.invoice_warn_msg,
                    'company_id': company_id,
                })
                self.env['bmair.history'].create(data_dict)

            if 'credit_limit' in vals:
                if credit_limit_old_val != partner.credit_limit:
                    data_dict.update({
                        'field_name': 'Credit Limit',
                        'old_value': credit_limit_old_val,
                        'new_value': partner.credit_limit,
                        'company_id': company_id,
                    })
                    self.env['bmair.history'].create(data_dict)

            if 'property_payment_term_id' in vals:
                if property_payment_term_id_old_val.id != partner.property_payment_term_id.id:
                    data_dict.update({
                        'field_name': 'Customer Payment Terms',
                        'old_value': property_payment_term_id_old_val.name,
                        'new_value': partner.property_payment_term_id.name,
                        'company_id': company_id,
                    })
                    self.env['bmair.history'].create(data_dict)

            if 'property_supplier_payment_term_id' in vals:
                if property_supplier_payment_term_id_old_val.id != partner.property_supplier_payment_term_id.id:
                    data_dict.update({
                        'field_name': 'Vendor Payment Terms',
                        'old_value': property_supplier_payment_term_id_old_val.name,
                        'new_value': partner.property_supplier_payment_term_id.name,
                        'company_id': company_id,
                    })
                    self.env['bmair.history'].create(data_dict)

            if 'property_product_pricelist' in vals:
                if property_product_pricelist_id_old_val.id != partner.property_product_pricelist.id:
                    data_dict.update({
                        'field_name': 'Pricelist',
                        'old_value': property_product_pricelist_id_old_val.name,
                        'new_value': partner.property_product_pricelist.name,
                        'company_id': company_id,
                    })
                    self.env['bmair.history'].create(data_dict)

            if 'property_account_position_id' in vals:
                if property_account_position_id_old_val.id != partner.property_account_position_id.id:
                    data_dict.update({
                        'field_name': 'Fiscal Position',
                        'old_value': property_account_position_id_old_val.name,
                        'new_value': partner.property_account_position_id.name,
                        'company_id': company_id,
                    })
                    self.env['bmair.history'].create(data_dict)

            if 'vat' in vals:
                if vat_old_val != partner.vat:
                    data_dict.update({
                        'field_name': 'VAT',
                        'old_value': vat_old_val,
                        'new_value': partner.vat,
                        'company_id': company_id,
                    })
                    self.env['bmair.history'].create(data_dict)
        return res
