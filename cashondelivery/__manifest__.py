# -*- coding: utf-8 -*-
{
    'name': 'Cashondelivery',
    'version': '10.0.1.0.0',    
    'author': 'Odoo Nodriza Tech (ONT)',
    'website': 'https://nodrizatech.com/',
    'category': 'Tools',
    'license': 'AGPL-3',
    'depends': ['base', 'sale', 'stock'],
    'data': [
        'data/ir_configparameter_data.xml',            
        'views/sale_order.xml',
        'views/stock_picking.xml',        
    ],
    'installable': True,
    'auto_install': False,    
}