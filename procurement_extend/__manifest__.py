# -*- coding: utf-8 -*-
{
    'name': "Procurement Extend",

    'summary': """
        Procurement Extend : Override cron function""",

    'description': """
        Long description of module's purpose
    """,

    'author': "B-informed",
    'website': "https://www.b-informed.nl",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['stock'],

    # always loaded
    'data': [
        'data/procurement_cron_data.xml'
        ],
    # only loaded in demonstration mode
    'demo': [],
}

