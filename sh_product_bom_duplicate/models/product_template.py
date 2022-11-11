# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models


class ProductTemplate(models.Model):
    _inherit = "product.template"


    def copy(self, default=None):

        prod_templ_id = self.id
        dup_product_template_id = super(
            ProductTemplate, self).copy(default=default)

        bom_obj = self.env["mrp.bom"].search(
            [("product_tmpl_id", "=", prod_templ_id)])
        if bom_obj:
            for record in bom_obj:

                record.copy(
                    default={"product_tmpl_id": dup_product_template_id.id})
        return dup_product_template_id


class ProductProduct(models.Model):
    _inherit = "product.product"


    def copy(self, default=None):

        prod_id = self.id
        dup_product_id = super(ProductProduct, self).copy(default=default)

        bom_obj = self.env["mrp.bom"].search([("product_id", "=", prod_id)])
        if bom_obj:
            for record in bom_obj:

                record.copy(default={"product_id": dup_product_id.id})
        return dup_product_id
