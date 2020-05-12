# -*- coding: utf-8 -*-
import logging
_logger = logging.getLogger(__name__)

from odoo import api, models, fields

class SaleOrder(models.Model):
    _inherit = 'sale.order'
                                
    @api.model    
    def cron_sale_orders_done_full_invoiced(self):
        sale_order_ids = self.env['sale.order'].search([('state', '=', 'sale'),('invoice_status', '=', 'invoiced')])        
        if sale_order_ids!=False:
            for sale_order_id in sale_order_ids:
                sale_order_id.state = 'done'    