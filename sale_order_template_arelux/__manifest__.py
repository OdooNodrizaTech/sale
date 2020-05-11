# -*- coding: utf-8 -*-
{
    'name': 'Sale Order Template Arelux',
    'version': '12.0.1.0.0',    
    'author': 'Odoo Nodriza Tech (ONT)',
    'website': 'https://nodrizatech.com/',
    'category': 'Tools',
    'license': 'AGPL-3',
    'depends': ['base', 'sale'],
    'data': [
        'data/ir_configparameter_data.xml',
        'views/sale_order_view.xml',
        'views/sale_portal_template.xml',
        'views/sale_order_template.xml',
    ],
    'installable': True,
    'auto_install': False,    
}