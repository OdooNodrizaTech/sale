# -*- coding: utf-8 -*-
from odoo import api, fields, models

import logging
_logger = logging.getLogger(__name__)

class SaleUserObjetive(models.Model):
    _name = 'sale.user.objetive'
    _description = 'Sale User Objetive'
    
    user_id = fields.Many2one(
        comodel_name='res.users',        
        string='Comercial',
    )
    date = fields.Date(        
        string='Fecha'
    )
    value = fields.Float(        
        string='Valor'
    )                            