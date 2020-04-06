# -*- coding: utf-8 -*-
import logging
_logger = logging.getLogger(__name__)

from openerp import api, models, fields
from openerp.exceptions import Warning
from datetime import datetime

class SaleOrder(models.Model):
    _inherit = 'sale.order'
                                
    @api.multi    
    def cron_sale_orders_done_full_invoiced(self, cr=None, uid=False, context=None):
        sale_order_ids = self.env['sale.order'].search([('state', '=', 'sale'),('invoice_status', '=', 'invoiced')])        
        if sale_order_ids!=False:
            for sale_order_id in sale_order_ids:
                sale_order_id.state = 'done'    