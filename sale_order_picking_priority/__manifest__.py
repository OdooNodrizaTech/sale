# -*- coding: utf-8 -*-
{
    'name': 'Sale Order Picking Priority',
    'version': '10.0.1.0.0',
    'author': 'Odoo Nodriza Tech (ONT)',
    'website': 'https://nodrizatech.com/',
    'category': 'Tools',
    'license': 'AGPL-3',
    'depends': ['base', 'sale', 'stock'],
    'data': [
        'views/sale_order.xml',
    ],
    'installable': True,
    'auto_install': False,
}