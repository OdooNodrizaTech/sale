# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models, _
from odoo.exceptions import Warning as UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def action_confirm(self):
        allow_action_confirm = True
        for item in self:
            if item.amount_total > 0 and item.payment_mode_id:
                if item.payment_mode_id.payment_method_id:
                    if item.payment_mode_id.payment_method_id.mandate_required:
                        # partner_id_check
                        partner_id_check = item.partner_invoice_id.id
                        if item.partner_invoice_id.parent_id:
                            partner_id_check = item.partner_invoice_id.parent_id.id
                        # account_banking_mandate_ids
                        items = self.env['account.banking.mandate'].search(
                            [
                                ('partner_bank_id.partner_id', '=', partner_id_check)
                            ]
                        )
                        if len(items) == 0:
                            allow_action_confirm = False
                            raise UserError(
                                _('The sale cannot be confirmed because there is no '
                                  'bank mandate created for the selected billing address')
                            )

        if allow_action_confirm:
            return super(SaleOrder, self).action_confirm()
