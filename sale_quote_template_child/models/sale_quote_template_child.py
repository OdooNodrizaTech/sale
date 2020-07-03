# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from openerp import api, models, fields

class SaleQuoteTemplateChild(models.Model):
    _name = 'sale.quote.template.child'

    name = fields.Char(
        string="Nombre"
    )
    template_id = fields.Many2one(
        comodel_name='sale.quote.template',         
        string='Plantilla presupuesto',
    )
    website_description = fields.Html(         
        string='Description',
        translate=True
    )     