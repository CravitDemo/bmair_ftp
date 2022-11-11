# -*- coding: utf-8 -*-
# Copyright 2019 B-Informed (<https://www.b-informed.nl>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': "Bmair - Account Reminder",
    'summary': """Bmair - Account Reminder""",
    'author': 'Cravit',
    'website': 'https://www.cravit.nl',
    'category': 'Technical Settings',
    'version': '14.0.1.0.0',
    'depends': [
        'account',
        'account_followup',
        'account_reports',
    ],
    'data': [
        'views/report_followup.xml',
        'views/res_partner_view.xml',

    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}
