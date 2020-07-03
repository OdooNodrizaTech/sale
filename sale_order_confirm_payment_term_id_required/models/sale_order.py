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
            if item.amount_total > 0 and item.payment_term_id.id == 0:
                allow_action_confirm = False
                raise Warning("Es necesario definir un plazo de pago")

        if allow_action_confirm == True:
            return super(SaleOrder, self).action_confirm()