# -*- coding: utf-8 -*-
from odoo import api, models, fields

class SaleOrderTemplateChild(models.Model):
    _name = 'sale.order.template.child'

    name = fields.Char(
        string="Nombre"
    )
    sale_order_template_id = fields.Many2one(
        comodel_name='sale.order.template',         
        string='Plantilla presupuesto',
    )
    website_description = fields.Html(         
        string='Description',
        translate=True
    )     