# -*- coding: utf-8 -*-

from odoo import models

class AccountMove(models.Model):
    _inherit = "account.move"

    def get_sale_order(self, invoice_origin):
        sale_order_id = self.env['sale.order'].search([('name', '=', invoice_origin)])
        if sale_order_id and sale_order_id.x_studio_reporting_date:
            return sale_order_id.x_studio_reporting_date.strftime('%d-%m-%Y')
        else:
            return False
        
    def get_contact_person(self, invoice_origin):
        sale_order_id = self.env['sale.order'].search([('name', '=', invoice_origin)])
        if sale_order_id and sale_order_id.partner_contact_id:
            return sale_order_id.partner_contact_id.name
        else:
            return False
        
    def get_our_contactperson(self, invoice_origin):
        sale_order_id = self.env['sale.order'].search([('name', '=', invoice_origin)])
        if sale_order_id and sale_order_id.user_id:
            return sale_order_id.user_id.name
        else:
            return self.user_id.name
        
        
