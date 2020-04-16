# -*- coding: utf-8 -*-
import logging
_logger = logging.getLogger(__name__)

from openerp import api, models, fields
from openerp.exceptions import Warning

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    opportunity_id = fields.Many2one(
        comodel_name='crm.lead', 
        string='Opportunity', 
        domain="[('type', '=', 'opportunity')]", 
        required=True
    )        
    
    @api.multi
    def action_confirm(self):
        allow_confirm = True
        #check
        for obj in self:            
            if obj.carrier_id.id>0 and obj.partner_shipping_id.id>0:
                if obj.partner_shipping_id.street==False:
                    allow_confirm = False
                    raise Warning("Es necesario definir una direccion para realizar el envio.\n")                
                elif obj.partner_shipping_id.city==False:
                    allow_confirm = False
                    raise Warning("Es necesario definir una ciudad/poblacion para realizar el envio.\n")                
                elif obj.partner_shipping_id.zip==False:
                    allow_confirm = False
                    raise Warning("Es necesario definir una codigo postal para realizar el envio.\n")                
                elif obj.partner_shipping_id.country_id.id==0:
                    allow_confirm = False
                    raise Warning("Es necesario definir una pais para realizar el envio.\n")                
                elif obj.partner_shipping_id.state_id.id==0:
                    allow_confirm = False
                    raise Warning("Es necesario definir una provincia para realizar el envio.\n")            
        #allow_confirm
        if allow_confirm==True:
            return super(SaleOrder, self).action_confirm()                                                                                                