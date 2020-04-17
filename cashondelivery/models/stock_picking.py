# -*- coding: utf-8 -*-
from openerp import api, models, fields
from datetime import datetime

import logging
_logger = logging.getLogger(__name__)

from lxml import etree

class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    total_cashondelivery = fields.Float( 
        string='Total contrareembolso pedido'
    )
        
    @api.model
    def create(self, values):
        return_object = super(StockPicking, self).create(values)
        #operations
        if return_object.origin!=False:
            sale_order_ids = self.env['sale.order'].sudo().search([('name', '=', return_object.origin)])
            if len(sale_order_ids)>0:
                sale_order_id = sale_order_ids[0]
                return_object.total_cashondelivery = sale_order_id.total_cashondelivery                    
        #return
        return return_object