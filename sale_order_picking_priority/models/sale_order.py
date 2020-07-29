# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    picking_priority = fields.Selection(
        [
            ('0', 'Not urgent'),
            ('1', 'Normal'),
            ('2', 'Urgent'),
            ('3', 'Very urgent'),
        ],
        default='1',
        string='Picking priority',
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
