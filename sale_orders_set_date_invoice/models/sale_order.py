# -*- coding: utf-8 -*-
import logging
_logger = logging.getLogger(__name__)

from openerp import api, models, fields
from openerp.exceptions import Warning
from datetime import datetime

class SaleOrder(models.Model):
    _inherit = 'sale.order'
                        
    date_invoice = fields.Date(
        string='Fecha factura', 
    )    
    
    @api.multi    
    def cron_sale_orders_set_date_invoice(self, cr=None, uid=False, context=None):                
        sale_order_ids = self.env['sale.order'].search(
            [
                ('date_invoice', '=', False), 
                ('invoice_status', '=', 'invoiced'),
                ('state', 'in', ('sale', 'done')),
                ('amount_untaxed', '>', 0)
             ]
        )
        if len(sale_order_ids)>0:
            for sale_order_id in sale_order_ids:
                date_invoice = False
                for invoice_id in sale_order_id.invoice_ids:
                    if invoice_id.type=='out_invoice':
                        if invoice_id.date_invoice!=False and date_invoice==False:
                            date_invoice = invoice_id.date_invoice
                #date_invoice                        
                if date_invoice!=False:
                    sale_order_id.date_invoice = date_invoice                    