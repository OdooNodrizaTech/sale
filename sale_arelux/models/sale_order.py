# -*- coding: utf-8 -*-
import logging
_logger = logging.getLogger(__name__)

from openerp import api, models, fields
from openerp.exceptions import Warning

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    @api.model
    def create(self, values):
        allow_create = True
        #operations
        if values['opportunity_id']==False and values['create_uid']!=1:
            allow_create = False
            raise Warning("Para crear un presupuesto es necesario definir un flujo")
        #allow_create
        if allow_create==True:
            return super(SaleOrder, self).create(values)        
    
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