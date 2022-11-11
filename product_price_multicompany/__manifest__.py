# -*- coding: utf-8 -*-
#################################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2017 B-informed Asia <info@B-informed.id>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#################################################################################

{
    "name" : "Product Price in multi company situation",
    "version" : "14.0.0.1",
    'license': 'AGPL-3',
    "author" : "B-informed Asia",
    "website": "http://www.b-informed.id",
    "category" : "Multi-company",
    "depends" : [
        'base',
        'sale',
    ],
    "demo" : [],
    "data" : [
        'views/product_template.xml'
    ],
    "qweb" : [],
    "images": ['static/description/banner.png'],
    'installable' : True,
    'active' : False,
    "price": "60.0",
    "currency": "EUR",
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: 