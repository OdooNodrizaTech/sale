# -*- coding: utf-8 -*-
from odoo import api, fields, models
from dateutil.relativedelta import relativedelta
from datetime import datetime
import decimal

import logging

_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    @api.one    
    def cron_action_regenerate_purchase_prices(self):
        if self.amount_total>0 and (self.state=='sale' or self.state=='done'):
            order_lines = {}
            for order_line in self.order_line:
                order_lines[order_line.product_id.id] = {
                    'is_delivery': order_line.is_delivery,                          
                    'purchase_price': 0,
                    'standard_price': order_line.product_id.standard_price,                     
                }
                        
            if self.picking_ids!=False:
                for picking_id in self.picking_ids:
                    if picking_id.state=='done':                        
                        if picking_id.move_lines!=False:
                            for move_line in picking_id.move_lines:
                                if move_line.quant_ids!=False:
                                    all_prices_same_cost = True
                                    last_price_cost = 0
                                    
                                    for quant_id in move_line.quant_ids:
                                        inventory_value_unit = 0                                                                                
                                        if quant_id.inventory_value!=False and quant_id.inventory_value>0:
                                            inventory_value_unit = quant_id.inventory_value/quant_id.qty
                                                                                        
                                            last_price_cost = quant_id.cost
                                            
                                            if last_price_cost>0 and last_price_cost!= quant_id.cost:
                                                all_prices_same_cost = False
                                        
                                        if move_line.product_id.id in order_lines:
                                            order_lines[move_line.product_id.id]['purchase_price'] = order_lines[move_line.product_id.id]['purchase_price'] + inventory_value_unit
                                    
                                    if all_prices_same_cost==True and move_line.product_id.id in order_lines:
                                        order_lines[move_line.product_id.id]['purchase_price'] = last_price_cost                                             
                                        
            for order_line_key in order_lines:
                if order_lines[order_line_key]['is_delivery']==False:
                    if order_lines[order_line_key]['purchase_price']==0:
                        order_lines[order_line_key]['purchase_price'] = order_lines[order_line_key]['standard_price']
            
            margin_order = 0                    
            for order_line in self.order_line:
                #Fix Mer4
                if order_line.product_id.id!=277:
                    order_line.purchase_price = order_lines[order_line.product_id.id]['purchase_price']
                                        
                    order_line.margin = order_line.price_subtotal - (order_line.purchase_price * order_line.qty_invoiced)
                    margin_order += order_line.margin                    
                    
            self.margin = margin_order
    
    @api.multi    
    def cron_action_regenerate_purchase_prices_send_orders(self, cr=None, uid=False, context=None):
        current_date = datetime.today()        
        start_date = current_date + relativedelta(months=-1)
        end_date = current_date
               
        sale_order_ids = self.env['sale.order'].search(
            [
                ('state', 'in', ('sale','done')),
                ('amount_total', '>', 0),
                ('confirmation_date', '>=', start_date.strftime("%Y-%m-%d")),
                ('confirmation_date', '<=', end_date.strftime("%Y-%m-%d"))
            ]
        )
        
        for sale_order_id in sale_order_ids:
            sale_order_id.cron_action_regenerate_purchase_prices()                                                                                                                 
                                                                    
    @api.multi    
    def cron_action_regenerate_purchase_prices_all(self, cr=None, uid=False, context=None):
        sale_order_ids = self.env['sale.order'].search(
            [
                ('state', 'in', ('sale','done')),
                ('amount_total', '>', 0)
            ]
        )
        
        for sale_order_id in sale_order_ids:
            sale_order_id.cron_action_regenerate_purchase_prices()                                                                                                                                                                                                               