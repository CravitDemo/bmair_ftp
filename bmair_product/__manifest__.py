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
    "name": "Enhancement for Bmair",
    "summary": "Enhancement of Bmair",
    "description": """
Enhancement of Bmair
    """,
    "website": "http://www.b-informed.nl/",
    'version': '1.1',
    "author": "B-Informed B.V.",
    "license": "AGPL-3",
    'category': 'Product',
    "depends": [
        'contacts','sale_management','purchase','l10n_nl','website_sale','stock',
    ],
    "qweb": [],
    'data': [
        'data/product_upload_cron.xml',
        'data/ir_sequence_data.xml',
        'security/ir.model.access.csv',
        'views/external_interface_view.xml',
        'wizard/product_wizard.xml',
        
    ]
}
