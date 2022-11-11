# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Maintain Object History',
    'version' : '1.1',
    'summary': 'Maintain Object History',
    'sequence': 999,
    'description': """
Maintain Object history based on field's onchange
""",
    'category': 'base',
    'author': 'Fortutech IMS',
    'website': 'http://www.fortutechims.com',
    'depends' : ['stock','product','sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/bmair_histoty_view.xml',
    ],

    'installable': True,
    'application': True,
    'auto_install': False,
}

