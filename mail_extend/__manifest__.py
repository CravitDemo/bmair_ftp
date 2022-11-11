# -*- coding: utf-8 -*-
{
    'name': "Mail Extend",

    'summary': """
        Mail Extend""",

    'description': """
        Mail Extend
    """,

    'author': "Cravit",
    'website': "https://www.cravit.nl",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'mail',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['mail'],

    # always loaded
    'data': [
        'data/data.xml',
    ],
}

