# -*- coding: utf-8 -*-
{
    'name' : 'MRP Workorder extend',
    'version' : '14.0.1',
    "author": "B-informed",
    'summary': 'Restricted serial number',
    'description': """
1. Once Manufacturing order serial number is added, in work order only that serial number should be available.
2. In consume product serial number , product that are already used in other move should not be available.    
3. Based on our last discussion , we need to make a option available in Manufacturing order,for traceable product to generate serial number in advance and also split manufacturing order (default feature of v14) and show that serial number in list view.
    """,
    'category': 'MRP',
    'depends' : ['mrp_workorder','stock'],
    'data': [
        #'security/ir.model.access.csv',
        'views/mrp_workorder_extend_view.xml',
        'reports/report_stockpicking_operations.xml',
        #'wizard/mrp_assign_serial_views.xml',
        'views/picking_view.xml',
    ],
    
    'installable': True,
    'application': True,
    'auto_install': False,
}
