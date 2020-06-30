# -*- coding: utf-8 -*-
from odoo import api, models, fields

import logging
_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.one
    def action_update_lines_prices_pricelist(self):
        if self.state in ['draft', 'sent']:
            if self.pricelist_id.id > 0 and self.order_line != False:
                for order_line in self.order_line:
                    order_line.product_uom_change()