# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def action_update_lines_prices_pricelist(self):
        self.ensure_one()
        if self.state in ['draft', 'sent']:
            if self.pricelist_id and self.order_line:
                for order_line in self.order_line:
                    order_line.product_uom_change()
