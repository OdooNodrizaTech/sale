# -*- coding: utf-8 -*-
from openerp import api, models, fields

import logging
_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    sale_order_sale_sum = fields.Monetary(
        compute='_get_sale_order_sale_sum',
        string='Sum total ventas'
    )
    sale_order_count_store = fields.Integer( 
        string='Count ventas'
    )    
    sale_order_pto_count = fields.Integer(
        compute='_sale_order_pto_count',
        string='Count pto'
    )
    
    @api.multi        
    def _get_sale_order_sale_sum(self):
        for partner in self:
            partner.sale_order_sale_sum = 0
            
            sale_order_ids = self.env['sale.order'].search(
                [
                    ('partner_id', 'child_of', partner.ids),
                    ('state', 'in', ('sale','done')),
                    ('amount_total', '>', 0),
                    ('claim', '=', False) 
                 ]
            )
            if sale_order_ids!=False:
                for sale_order_id in sale_order_ids:
                    partner.sale_order_sale_sum = partner.sale_order_sale_sum + sale_order_id.amount_untaxed
    
    @api.multi
    def _sale_order_pto_count(self):
        for partner in self:            
            sale_order_ids = self.env['sale.order'].search(
                [
                    ('claim', '=', False),
                    ('partner_id', 'child_of', partner.ids),
                    '|', 
                    '&', 
                    ('state', 'in', ('sale','done')), 
                    ('amount_total', '=', 0), 
                    '&', 
                    ('state', 'in', ('draft','sent')), 
                    ('amount_total', '>', 0)
                ]
            )            
            partner.sale_order_pto_count = len(sale_order_ids)
            
    @api.model
    def create(self, values):
        record = super(ResPartner, self).create(values)        
        #state_id
        if record.state_id.id>0:        
            product_pricelist_ids = self.env['product.pricelist'].search(
                [
                    ('ar_qt_activity_type', '=', record.ar_qt_activity_type),
                    ('ar_qt_customer_type', '=', record.ar_qt_customer_type),
                    ('state_ids', 'in', (record.state_id.id))
                ]
            )
            if len(product_pricelist_ids)>0:
                product_pricelist_id = product_pricelist_ids[0]
                record.property_product_pricelist = product_pricelist_id.id                                   
            else:
                record.property_product_pricelist = 1                
        #return                
        return record
    
    @api.multi    
    def cron_operations_res_partners(self, cr=None, uid=False, context=None):
        #reset all 0
        self.env.cr.execute("UPDATE res_partner SET sale_order_count_store = 0 WHERE id > 0")
        #update only with sales                    
        self.env.cr.execute("UPDATE res_partner SET sale_order_count_store = (SELECT COUNT(so.id) AS total FROM sale_order AS so WHERE so.state IN ('sale', 'done') AND so.amount_total > 0 AND so.claim = False AND (so.partner_id = res_partner.id OR so.partner_invoice_id = res_partner.id OR so.partner_id IN (SELECT rp.id FROM res_partner AS rp WHERE rp.parent_id = res_partner.id) OR so.partner_invoice_id IN (SELECT rp.id FROM res_partner AS rp WHERE rp.parent_id = res_partner.id))) WHERE id IN (SELECT DISTINCT(so.partner_id) FROM sale_order AS so WHERE so.amount_total > 0 AND so.claim = False And so.state IN ('sale', 'done'))")                
            