# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.tools.misc import xlwt
from io import BytesIO
import base64
from datetime import datetime
import tempfile
import csv
import requests
import ftplib

#----------------------------------------------------------
# Products
#----------------------------------------------------------
class ProductTemplate(models.Model):
    _inherit = "product.template"
    
    def upload_product_export(self):
        header = ['Article number (Internal reference)', 'Article description (product name)', 'Main product categorie (Product categorie)', 'Sub product category (child categorie 1)', 'Sub product category (child categorie 2)','Warehouse location']
        
        filename = 'Nicelabel_products.csv'
        
#         sequence = self.env['ir.sequence'].next_by_code('external.interface') or _('PC_New')
#         filename = '%s.csv'%(sequence)
        with open('/tmp/%s'%(filename), 'w', newline='') as file:
            writer = csv.writer(file,delimiter=";")
            writer.writerow(header)
            for product_id in self:
                prodgroup = prodgroupex = prodgroupsub = ''
                last_categ = product_id.categ_id
                if product_id.categ_id.parent_id:
                    sec_last_categ = product_id.categ_id.parent_id
                    if sec_last_categ.parent_id:
                        third_last_categ = sec_last_categ.parent_id
                        if third_last_categ.parent_id:
                            fourth_last_categ = third_last_categ.parent_id
                            if fourth_last_categ.parent_id:
                                fifth_last_categ = fourth_last_categ.parent_id
                                if fifth_last_categ.parent_id:
                                    sixth_last_categ = fifth_last_categ.parent_id
                                    #lsat search
                                    prodgroup = fifth_last_categ.parent_id.name
                                    prodgroupex = fifth_last_categ.name
                                    prodgroupsub = fourth_last_categ.name
                                else:
                                    prodgroup = fourth_last_categ.parent_id.name
                                    prodgroupex = fourth_last_categ.name
                                    prodgroupsub = third_last_categ.name
                            else:
                                prodgroup = third_last_categ.parent_id.name
                                prodgroupex = third_last_categ.name
                                prodgroupsub = sec_last_categ.name
                        else:
                            prodgroup = sec_last_categ.parent_id.name
                            prodgroupex = sec_last_categ.name
                            prodgroupsub = product_id.categ_id.name
                    else:
                        prodgroup = product_id.categ_id.parent_id.name
                        prodgroupex = product_id.categ_id.name
                else:
                    prodgroup = last_categ.name
                    
                if len(product_id.product_variant_ids) == 1:
                    product_location = self.env['stock.putaway.rule'].search([
                        ('product_id', '=', product_id.product_variant_ids[0].id)
                    ],limit=1)
                    p_location = ''
                    if product_location and product_location.location_out_id: 
                        p_location = product_location.location_out_id.name
                    product_list = [product_id.default_code, product_id.name, prodgroup, prodgroupex, prodgroupsub, p_location]
                    writer.writerow(product_list)
                else:
                    for product in product_id.product_variant_ids:
                        product_location = self.env['stock.putaway.rule'].search([
                            ('product_id', '=', product.id)
                        ],limit=1)
                        p_location = ''
                        if product_location and product_location.location_out_id: 
                            p_location = product_location.location_out_id.name
                        product_list = [product.default_code, product.name, prodgroup, prodgroupex, prodgroupsub, p_location]
                        writer.writerow(product_list)
        file.close()
        ftp_location = self.env['external.interface'].search([],limit=1)
        if ftp_location:
            myfile = open('/tmp/%s'%(filename), 'rb')
            try:
                ftps = ftplib.FTP_TLS(ftp_location.ftp_location,ftp_location.user_name, ftp_location.pwd)
                ftps.prot_p()
                ftps.cwd('/upload')
                ftps.storbinary('STOR %s' % filename, myfile)
                ftps.close()
                msg_succ = "Message LOG : File sent successfully "  + str(filename)
                ftp_location.message_post(body=msg_succ)
            except Exception as error:
                msg_error = "ERROR LOG : " + str(error)
                ftp_location.message_post(body=msg_error)
                pass
        return True
    
    def cron_product_export_upload(self):
        product_ids = self.search([])
        product_ids.upload_product_export()
        return True


#     def get_product_accounts(self, fiscal_pos=None):
#         accounts = self._get_product_accounts()
#         if not fiscal_pos:
#             fiscal_pos = self.env['account.fiscal.position']
#         return fiscal_pos.map_accounts(accounts)


# class ProductProduct(models.Model):
#     _inherit = "product.product"

