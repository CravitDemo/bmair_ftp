# -*- coding: utf-8 -*-

{
    "name": "Report Header Footer",
    "summary": "Custom header footer ",
    "description": """
Custom footer for multicompanies for Bmair    """,
    "website": "http://www.b-informed.nl/",
    'version': '14.0.1.0.0',
    "author": "B-Informed B.V.",
    "license": "AGPL-3",
    'category': 'report',
    "depends": [
        'web', 'purchase', 'bmair_sales', 'account_intrastat', 'delivery', 'stock', 'sale_stock',
    ],
    "qweb": [],
    'data': [
        'data/data.xml',
        'reports/report_header_footer_view.xml',
        'reports/purchase_order_report.xml',
        'reports/report_header_view.xml',
        'reports/sale_order_report_view.xml',
        'reports/invoice_report_view.xml',
        'reports/delivery_slip_view.xml',
    ]
}

