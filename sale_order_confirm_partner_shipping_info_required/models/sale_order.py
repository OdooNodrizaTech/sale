# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, models, fields
from odoo.exceptions import Warning

import logging
_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def action_confirm(self):
        allow_action_confirm = True

        for item in self:
            if item.carrier_id.id > 0 and item.partner_shipping_id.id > 0:
                if item.partner_shipping_id.street == False:
                    allow_action_confirm = False
                    raise Warning("Es necesario definir una direccion para realizar el envio")
                elif item.partner_shipping_id.city == False:
                    allow_action_confirm = False
                    raise Warning("Es necesario definir una ciudad/poblacion para realizar el envio")
                elif item.partner_shipping_id.zip == False:
                    allow_action_confirm = False
                    raise Warning("Es necesario definir una codigo postal para realizar el envio.\n")
                elif item.partner_shipping_id.country_id == 0:
                    allow_action_confirm = False
                    raise Warning("Es necesario definir una pais para realizar el envion")
                elif item.partner_shipping_id.state_id == 0:
                    allow_action_confirm = False
                    raise Warning("Es necesario definir una provincia para realizar el envion")

        if allow_action_confirm == True:
            return super(SaleOrder, self).action_confirm()