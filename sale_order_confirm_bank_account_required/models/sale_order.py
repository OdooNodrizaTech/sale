# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models, _
from odoo.exceptions import Warning


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def action_confirm(self):
        allow_action_confirm = True
        for item in self:
            if item.amount_total>0 and item.payment_mode_id:
                if item.payment_mode_id.payment_method_id:
                    if item.payment_mode_id.payment_method_id.bank_account_required:
                        # partner_id_check
                        partner_id_check = item.partner_invoice_id.id
                        if item.partner_invoice_id.parent_id:
                            partner_id_check = item.partner_invoice_id.parent_id.id
                        # res_partner_bank_ids
                        res_partner_bank_ids = self.env['res.partner.bank'].search(
                            [
                                ('partner_id', '=', partner_id_check)
                            ]
                        )
                        if len(res_partner_bank_ids) == 0:
                            allow_action_confirm = False
                            raise Warning(_('The sale cannot be confirmed because there is no account created for the selected billing address'))

        if allow_action_confirm:
            return super(SaleOrder, self).action_confirm()