# -*- coding: utf-8 -*-
{
    'name': 'Sale Orders Set Date Invoice',
    'version': '10.0.1.0.0',    
    'author': 'Odoo Nodriza Tech (ONT)',
    'website': 'https://nodrizatech.com/',
    'category': 'Tools',
    'license': 'AGPL-3',
    'depends': ['base', 'sale', 'account'],
    'data': [        
        'data/ir_cron.xml',
    ],
    'installable': True,
    'auto_install': False,    
}