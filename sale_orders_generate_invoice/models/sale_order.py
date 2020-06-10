# -*- coding: utf-8 -*-
import logging
_logger = logging.getLogger(__name__)

from odoo import api, models, fields
from datetime import datetime

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    @api.one    
    def action_account_invoice_not_create_partner_without_vat(self):
        return True
    
    @api.one
    def allow_generate_invoice(self):
        #check
        allow_generate_invoice = False
        need_delivery_something = False
        
        if self.invoice_status=='to invoice':
            total_qty_to_invoice = 0
                            
            for order_line in self.order_line:
                if order_line.product_id.invoice_policy=='order':                        
                    total_qty_to_invoice = total_qty_to_invoice + order_line.product_uom_qty
                else:
                    total_qty_to_invoice = total_qty_to_invoice + order_line.qty_delivered
                    need_delivery_something = True                
            
            if total_qty_to_invoice>0:
                current_date = fields.Datetime.from_string(str(datetime.today().strftime("%Y-%m-%d %H:%M:%S")))
                allow_generate_invoice = False
                
                if need_delivery_something==True:
                    stock_picking_date_done = False
                    all_stock_picking_done = True
                    # picking_ids
                    for picking_id in self.picking_ids:
                        if picking_id.picking_type_id.code == 'outgoing':
                            if picking_id.state == 'done':
                                stock_picking_date_done = picking_id.date_done
                            else:
                                all_stock_picking_done = False
                    #operations
                    if all_stock_picking_done==True and stock_picking_date_done!=False:
                        allow_generate_invoice = True                                                                                                        
                else:
                    allow_generate_invoice = True
                
                #check nif
                if allow_generate_invoice==True:
                    if self.partner_invoice_id.vat==False:
                        allow_generate_invoice = False
                        self.action_account_invoice_not_create_partner_without_vat()#Fix Slack                        
                        
                        _logger.info('El pedido '+str(self.name)+' no se puede facturar porque el cliente NO tiene CIF')
        #return
        return allow_generate_invoice
          
    @api.model    
    def cron_action_orders_generate_invoice(self):        
        current_date = datetime.today()
        allow_generate_invoices = True
        
        if current_date.day==31 and current_date.month==12:
            allow_generate_invoices = False
            
        if current_date.day==1 and current_date.month==1:
            allow_generate_invoices = False
        
        if allow_generate_invoices==True:
            sale_order_ids = self.env['sale.order'].search(
                [
                    ('state', '=', 'sale'),
                    ('amount_total', '>', 0),
                    ('payment_mode_id', '!=', False), 
                    ('invoice_status', '=', 'to invoice'),
                    ('disable_autogenerate_create_invoice', '=', False)
                 ]
            )
            if sale_order_ids!=False:
                #group_by_partner_id
                sale_order_ids_by_partner_id = {}
                for sale_order_id in sale_order_ids:
                    #check
                    allow_generate_invoice = sale_order_id.allow_generate_invoice()[0]                    
                    #add if need
                    if allow_generate_invoice==True:                    
                        if sale_order_id.partner_invoice_id.id not in sale_order_ids_by_partner_id:
                            sale_order_ids_by_partner_id[sale_order_id.partner_invoice_id.id] = []
                        #add_sale_order_ids
                        sale_order_ids_by_partner_id[sale_order_id.partner_invoice_id.id].append(sale_order_id.id)
                
                if len(sale_order_ids_by_partner_id)>0:                
                    for partner_id in sale_order_ids_by_partner_id:
                        ids = sale_order_ids_by_partner_id[partner_id]                    
                        sale_order_ids_get = self.env['sale.order'].search([('id', 'in', ids)])
                        return_invoice_create = sale_order_ids_get.action_invoice_create()
                        #sale_order_ids
                        for sale_order_id_get in sale_order_ids_get:
                            sale_order_id_get.state = 'done'
                        #invoice_ids
                        invoice_id = return_invoice_create[0]
                        account_invoice_id = self.env['account.invoice'].browse(invoice_id)
                        #action_auto_create
                        account_invoice_id.action_auto_create()                        
                        #operations
                        if account_invoice_id.amount_total>0:
                            account_invoice_id.action_invoice_open()
                            #action_auto_open
                            account_invoice_id.action_auto_open()                                                                        
                            #send mail
                            account_invoice_id.cron_account_invoice_auto_send_mail_item()