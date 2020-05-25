# -*- coding: utf-8 -*-
from odoo import api, models, fields

import logging
_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    picking_priority = fields.Selection(
        [
            ('0', 'No urgente'),
            ('1', 'Normal'),
            ('2', 'Urgente'),
            ('3', 'Muy Urgente'),
        ],
        default='1',
        string='Prioridad albaran',
    )

    @api.multi
    def action_confirm(self):
        return_data = super(SaleOrder, self).action_confirm()
        # operations
        for item in self:
            if item.state == 'sale':
                for picking_id in item.picking_ids:
                    picking_id.priority = item.picking_priority
        # return
        return return_data