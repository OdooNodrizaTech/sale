# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models, fields, _
from odoo.exceptions import Warning as UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    total_cashondelivery = fields.Float(
        string='Total cashondelivery'
    )
    payment_mode_id_is_cashondelivery = fields.Boolean(
        string='Payment mode id is cashondelivery?',
        compute='_compute_payment_mode_id_is_cashondelivery',
        default=False
    )

    @api.multi
    def _compute_payment_mode_id_is_cashondelivery(self):
        self.ensure_one()
        if self.payment_mode_id.id > 0:
            self.payment_mode_id_is_cashondelivery = self.payment_mode_id.is_cashondelivery

    @api.multi
    def action_confirm(self):
        allow_confirm = True
        #check
        for item in self:
            if item.amount_total>0:
                if item.payment_mode_id.id>0:
                    if item.payment_mode_id_is_cashondelivery==True:
                        if item.payment_mode_id.minimum_amount_cashondelivery>0 and item.total_cashondelivery<item.payment_mode_id.minimum_amount_cashondelivery:
                            allow_confirm = False
                            raise UserError(_('Cash on delivery cannot be confirmed with a cash on delivery total of less than %s') % (item.payment_mode_id.minimum_amount_cashondelivery))
        #allow_confirm
        if allow_confirm==True:
            return super(SaleOrder, self).action_confirm()