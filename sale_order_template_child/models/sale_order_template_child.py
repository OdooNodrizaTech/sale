# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields


class SaleOrderTemplateChild(models.Model):
    _name = 'sale.order.template.child'
    _description = 'Sale Order Template Child'

    name = fields.Char(
        string="Name"
    )
    sale_order_template_id = fields.Many2one(
        comodel_name='sale.order.template',         
        string='Order template',
    )
    website_description = fields.Html(         
        string='Description',
        translate=True
    )     