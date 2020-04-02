# -*- coding: utf-8 -*-
import logging
_logger = logging.getLogger(__name__)

from openerp import api, models, fields
from openerp.exceptions import Warning

class SaleOrder(models.Model):
    _inherit = 'sale.order'            
    
    @api.multi
    def action_confirm(self):
        #check
        allow_confirm = True
        for obj in self:            
            if obj.need_check_credit_limit==True:
                future_max_credit_limit_allow = obj.max_credit_limit_allow - obj.amount_total
                if future_max_credit_limit_allow<=0:
                    allow_confirm = False
                    raise Warning("No se puede confirmar la venta porque no hay credito disponible o el importe total de esta venta es superior al credito disponible ("+str(future_max_credit_limit_allow)+")")        
        #allow_confirm
        if allow_confirm==True:
            return super(SaleOrder, self).action_confirm()