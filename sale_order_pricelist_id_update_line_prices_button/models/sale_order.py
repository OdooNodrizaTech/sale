# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def action_update_lines_prices_pricelist(self):
        for item in self:
            if item.state in ['draft', 'sent']:
                if item.pricelist_id and item.order_line:
                    for order_line in item.order_line:
                        order_line.product_uom_change()
