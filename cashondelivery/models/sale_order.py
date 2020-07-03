# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import logging
_logger = logging.getLogger(__name__)

from odoo import api, models, fields
from odoo.exceptions import Warning

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    total_cashondelivery = fields.Float( 
        string='Total contrareembolso'
    )
    
    @api.multi
    def action_confirm(self):
        allow_confirm = True
        #config
        account_payment_mode_id_cashondelivery = int(self.env['ir.config_parameter'].sudo().get_param('account_payment_mode_id_cashondelivery'))
        #check
        for obj in self:
            if obj.amount_total>0:                                        
                if account_payment_mode_id_cashondelivery==self.payment_mode_id.id:
                    if self.total_cashondelivery<10:
                        allow_confirm = False
                        raise Warning("No se puede confirmar la venta de contrareembolso con un total_contrareembolso menor de 10")                           
        #allow_confirm
        if allow_confirm==True:
            return super(SaleOrder, self).action_confirm()