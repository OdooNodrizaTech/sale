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
    
    @api.multi
    def force_assign(self):
        #operations
        for obj in self:
            if obj.group_id.id>0:
                procurement_order_ids = self.env['procurement.order'].sudo().search([('group_id', '=', obj.group_id.id)])
                if len(procurement_order_ids)>0:
                    procurement_order_id = procurement_order_ids[0]
                    if procurement_order_id.sale_line_id.id>0:
                        obj.total_cashondelivery = procurement_order_id.sale_line_id.order_id.total_cashondelivery                                            
        #return
        return super(StockPicking, self).force_assign()