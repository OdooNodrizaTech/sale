# -*- coding: utf-8 -*-
import logging
_logger = logging.getLogger(__name__)

from openerp import fields, models, api, _

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    link_tracker_id = fields.Many2one(
        comodel_name='link.tracker', 
        string='Link Tracker Id'
    )

    @api.model
    def create(self, values):
        return_object = super(SaleOrder, self).create(values)
        # operations
        if return_object.access_token != False:
            return_object.action_generate_sale_order_link_tracker()
        # return
        return return_object

    @api.one    
    def action_generate_sale_order_link_tracker(self):        
        if self.link_tracker_id.id==0 and self.access_token!=False:
            web_base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
            url = web_base_url+'/quote/'+str(self.id)+'/'+str(self.access_token)
            link_tracker_vals = {
                'title': self.name,    
                'url': url
            }
            link_tracker_obj = self.env['link.tracker'].sudo().create(link_tracker_vals)
            if link_tracker_obj!=False:
                self.link_tracker_id = link_tracker_obj.id
        #return
        return True                    
         
    @api.multi    
    def cron_generate_sale_order_link_tracker(self, cr=None, uid=False, context=None):        
        sale_order_ids = self.env['sale.order'].search([('link_tracker_id', '=', False)], limit=2)
        if sale_order_ids!=False:
            for sale_order_id in sale_order_ids:
                sale_order_id.action_generate_sale_order_link_tracker()                                                           