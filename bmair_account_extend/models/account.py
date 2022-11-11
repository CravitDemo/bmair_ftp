# -*- coding: utf-8 -*-
from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    def bmair_create_line_auto_complete(self, po_id):
        self.write({'purchase_id':po_id.id})
        union_tbl_id = self.env['purchase.bill.union'].search([('purchase_order_id', '=', po_id.id)],limit=1)
        self.purchase_vendor_bill_id = union_tbl_id and union_tbl_id.id

        if self.purchase_vendor_bill_id.vendor_bill_id:
            self.invoice_vendor_bill_id = self.purchase_vendor_bill_id.vendor_bill_id
            self._onchange_invoice_vendor_bill()
        elif self.purchase_vendor_bill_id.purchase_order_id:
            self.purchase_id = self.purchase_vendor_bill_id.purchase_order_id
        self.purchase_vendor_bill_id = False
        self.partner_id = self.purchase_id.partner_id
        self.fiscal_position_id = self.purchase_id.fiscal_position_id
        self.invoice_payment_term_id = self.purchase_id.payment_term_id
        self.currency_id = self.purchase_id.currency_id

        # Copy purchase lines.
        po_lines = self.purchase_id.order_line - self.line_ids.mapped('purchase_line_id')
        new_lines = self.env['account.move.line']
        for line in po_lines.filtered(lambda l: not l.display_type):
            line_dd = line._prepare_account_move_line(self)
            prod_id = line_dd.get('product_id')
            get_prod_id = self.env['product.product'].search([('id','=',int(prod_id))])
            fiscal_position = self.fiscal_position_id
            accounts = get_prod_id.product_tmpl_id.get_product_accounts(fiscal_pos=fiscal_position)
            if self.is_sale_document(include_receipts=True):
                acc_id = accounts['income']
            elif self.is_purchase_document(include_receipts=True):
                acc_id = accounts['expense']
 
            line_dd.update({'account_id':acc_id.id, 'exclude_from_invoice_tab': False})
            self.write({'invoice_line_ids': [(0, 0, line_dd)]})

        origins = set(self.line_ids.mapped('purchase_line_id.order_id.name'))
        self.invoice_origin = ','.join(list(origins))
        for lline in self.invoice_line_ids:
            lline.account_id = lline._get_computed_account()
        self.purchase_id = False
        #self.original_amount = self.amount_total
        self.write({'purchase_id': False})

    def action_auto_complete(self):
        for rec in self:
            po_id = self.env['purchase.order'].search([('partner_id','=',rec.partner_id.id),('state','in',('purchase', 'done'))],limit=1)
            if po_id:
                rec.bmair_create_line_auto_complete(po_id)

