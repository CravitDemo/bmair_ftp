# -*- coding: utf-8 -*-

# Part of FlexERP. See LICENSE file for full copyright and licensing details.

{
    'name': 'Followup Email - Send to Different Email Address',
    'version': '13.0.1.0',
    'category': 'Accounting',
    'depends': ['account_followup'],
    'license': 'OPL-1',
    'price': 20.00,
    'currency': 'EUR',
    'summary': """This module adds the field 'Statement of Account Email' to partner form. When filled this email is used for follow-up emails instead of the regular email address.
               """,
    'images': ['static/description/statement_new_field.png'],
    'description': """
       Add specific email address for sending out follow-up emails.
    """,
    'author': 'FlexERP - info@flexerp.dk ',
    'maintainer': 'FlexERP - info@flexerp.dk ',
    'website': 'www.flexerp.dk',

    'data': [
        'views/template.xml',
        'views/res_partner_view.xml',
        'views/report_followup.xml'
    ],
    'installable' : True,
    'application' : False,
    'auto_install' : False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
