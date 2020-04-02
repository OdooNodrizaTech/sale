# -*- coding: utf-8 -*-
import logging
_logger = logging.getLogger(__name__)

from openerp import api, models, fields
from openerp.exceptions import Warning

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    @api.multi
    def action_confirm(self):
        allow_confirm = True
        #check
        for obj in self:            
            if obj.partner_id.vat==False:
                allow_confirm = False
                raise Warning("Es necesario definir VAT para el cliente antes de validar el pedido de venta.\n")            
        #allow_confirm
        if allow_confirm==True:
            return super(SaleOrder, self).action_confirm()