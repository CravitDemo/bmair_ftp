# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Resham Kumari - B-informed B.V.
#    Copyright 2017 B-informed B.V.
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
##############################################################################

{
    "name": "Enhancement of Field service Management for Bmair",
    "summary": "Enhancement of Field service Management for Bmair",
    "description": """
Enhancement of Field service Management for Bmair
    """,
    "website": "http://www.b-informed.nl/",
    'version': '1.1',
    "author": "B-Informed B.V.",
    "license": "AGPL-3",
    'category': 'Operations/Field Service',
    "depends": [
        'bmair_contact','industry_fsm_stock',
    ],
    "qweb": [],
    'data': [
        'security/security_group.xml',
        'security/ir.model.access.csv',
        "views/res_users_view.xml",
        "views/fsm_machine_view.xml",
        'views/fsm_view.xml',
        'views/orderpoint_view.xml',
        'views/fsm_product_view.xml',
        'views/fsm_sales_order.xml',
    ]
}

