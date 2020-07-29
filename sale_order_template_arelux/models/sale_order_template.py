# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields

class SaleOrderTemplate(models.Model):
    _inherit = 'sale.order.template'
    
    delivery_carrier_id = fields.Many2one(
        comodel_name='delivery.carrier',
        string='Carrier id'
    )
