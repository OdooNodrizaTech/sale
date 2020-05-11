# -*- coding: utf-8 -*-
from odoo import api, models, fields

class SaleOrderTemplate(models.Model):
    _inherit = 'sale.order.template'
    
    delivery_carrier_id = fields.Many2one(
        comodel_name='delivery.carrier', 
        string='Metodo de envio',
    )