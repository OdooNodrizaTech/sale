# -*- coding: utf-8 -*-
{
    'name': 'Sale Order Template Child',
    'version': '12.0.1.0.0',    
    'author': 'Odoo Nodriza Tech (ONT)',
    'website': 'https://nodrizatech.com/',
    'category': 'Tools',
    'license': 'AGPL-3',
    'depends': ['base', 'crm_claim', 'sale'],
    'data': [
        'views/sale_order.xml',
        'views/sale_order_template_child.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'auto_install': False,    
}