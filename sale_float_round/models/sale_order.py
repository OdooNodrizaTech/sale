# -*- coding: utf-8 -*-
from odoo import api, fields, models

import logging

_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = 'sale.order'                                
   
    @api.multi    
    def cron_odoo_float_round(self, cr=None, uid=False, context=None):
        self.env.cr.execute("UPDATE sale_order SET amount_total = ROUND(amount_total::numeric,2) WHERE id IN (SELECT id FROM sale_order WHERE amount_total <> ROUND(amount_total::NUMERIC,2))")