# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import logging
_logger = logging.getLogger(__name__)

from odoo import fields, models, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    link_tracker_id = fields.Many2one(
        comodel_name='link.tracker', 
        string='Link Tracker Id'
    )

    @api.one    
    def action_generate_sale_order_link_tracker(self):        
        if self.link_tracker_id.id==0:
            web_base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
            url = web_base_url+'/quote/'+str(self.id)+'/'+str(self.access_token)
            link_tracker_vals = {
                'title': self.name,    
                'url': url,                
            }
            link_tracker_obj = self.env['link.tracker'].sudo().create(link_tracker_vals)
            if link_tracker_obj!=False:
                self.link_tracker_id = link_tracker_obj.id
        #return
        return True                    
         
    @api.multi    
    def cron_generate_sale_order_link_tracker(self, cr=None, uid=False, context=None):        
        sale_order_ids = self.env['sale.order'].search([('link_tracker_id', '=', False)], limit=1000)        
        if sale_order_ids!=False:
            for sale_order_id in sale_order_ids:
                sale_order_id.action_generate_sale_order_link_tracker()                                                           