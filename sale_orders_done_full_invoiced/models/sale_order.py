# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model
    def cron_sale_orders_done_full_invoiced(self):
        items = self.env['sale.order'].search(
            [
                ('state', '=', 'sale'),
                ('invoice_status', '=', 'invoiced')
            ]
        )
        if items:
            for item in items:
                item.state = 'done'
