# -*- coding: utf-8 -*-
import logging
_logger = logging.getLogger(__name__)

from odoo import api, models, fields

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    sale_order_template_child_id = fields.Many2one(
        comodel_name='sale.order.template.child', 
        string='Subplantilla de presupuesto'
    )                                                                                                                                                   