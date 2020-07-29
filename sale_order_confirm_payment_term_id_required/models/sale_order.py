# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models, _
from odoo.exceptions import Warning


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def action_confirm(self):
        allow_action_confirm = True
        for item in self:
            if item.amount_total > 0 and item.payment_term_id.id == 0:
                allow_action_confirm = False
                raise Warning(_('It is necessary to define a payment term'))

        if allow_action_confirm:
            return super(SaleOrder, self).action_confirm()
