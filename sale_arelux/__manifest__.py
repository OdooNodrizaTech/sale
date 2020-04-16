# -*- coding: utf-8 -*-
{
    'name': 'Sale Arelux',
    'version': '10.0.1.0.0',    
    'author': 'Odoo Nodriza Tech (ONT)',
    'website': 'https://nodrizatech.com/',
    'category': 'Tools',
    'license': 'AGPL-3',
    'depends': ['base', 'sale', 'sale_crm', 'delivery'],
    'data': [
        'data/ir_cron.xml',
        'views/res_partner.xml',
    ],
    'installable': True,
    'auto_install': False,    
}