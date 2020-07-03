# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    'name': 'Sale Quote Template Child',
    'version': '10.0.1.0.0',    
    'author': 'Odoo Nodriza Tech (ONT)',
    'website': 'https://nodrizatech.com/',
    'category': 'Tools',
    'license': 'AGPL-3',
    'depends': ['base', 'crm_claim', 'sale', 'website_quote'],
    'data': [
        'views/sale_order.xml',
        'views/sale_quote_template_child.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'auto_install': False,    
}