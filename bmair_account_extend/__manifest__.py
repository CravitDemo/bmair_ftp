# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Fortutech IMS Pvt. Ltd.
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
    "name": "Account Extend for BMair",
    "summary": "Account Extend for BMair",
    "description": """
Account Extend for BMair
    """,
    "website": "http://www.fortutechims.com/",
    'version': '1.0',
    "author": "Fortutech IMS Pvt. Ltd.",
    "license": "AGPL-3",
    'category': 'Accounting',
    "depends": [
        'account', 'partner_autocomplete',
    ],
    "qweb": [],
    'data': [
        'views/account_view.xml',
    ]
}

