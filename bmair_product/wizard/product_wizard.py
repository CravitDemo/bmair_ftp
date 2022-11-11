# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.tools.misc import xlwt
from io import BytesIO
import base64
from datetime import datetime
import tempfile
import csv
import requests

# feature_5560_Nicelabel_export

class ProductExportWizard(models.TransientModel):
    _name = 'product.export.wizard'
    _description = "Product export wizard" 
    
    export_file = fields.Binary('Download File')
    file_name = fields.Char('File Name')
    valuation_printed = fields.Boolean('Valuation Report Printed')
    
    def product_create_datasheet(self):
        if self.env.context.get('active_ids'):
            product_ids = self.env['product.template'].browse(self.env.context.get('active_ids'))
        else:
            product_ids = self.env['product.template'].search([])
        header = ['Article number (Internal reference)', 'Article description (product name)', 'Main product categorie (Product categorie)', 'Sub product category (child categorie 1)', 'Sub product category (child categorie 2)','Warehouse location']
        
        filename = 'Nicelabel_products_%s.csv'%(datetime.now())
        with open('/tmp/%s'%(filename), 'w', newline='') as file:
            writer = csv.writer(file,delimiter=";")
            writer.writerow(header)
            for product_id in product_ids:
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
          
        f = open('/tmp/%s'%(filename), 'rb')
        file_base64 = base64.b64encode(f.read()).decode('ascii')
        self.file_name = filename
        self.export_file = file_base64
        self.valuation_printed = True
        return {
                'view_mode': 'form',
                'res_id': self.id,
                'res_model': 'product.export.wizard',
                'view_type': 'form',
                'type': 'ir.actions.act_window',
                'context': {},
                'target': 'new',
        }
    
