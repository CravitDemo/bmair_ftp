# -*- coding: utf-8 -*-
{
    "name": "Bmair Sale Changes",
    "summary": "Sales changes",
    "version": "14.0.1.0.0",
    "category": 'Sales/Sales',
    "website": "http://www.b-informed.nl/",
    'version': '1.1',
    "author": "B-Informed B.V.",
    "license": "AGPL-3",
    "installable": True,
    "depends": ["sale", "sale_stock"],
    "data": [
        "views/sale_view.xml",
        "views/account_view.xml",
        'report/sale_order_report_templates.xml',
    ],
}
