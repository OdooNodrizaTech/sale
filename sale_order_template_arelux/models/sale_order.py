# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.http import request


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    payment_acquirer_type_amount_paid = fields.Selection(
        selection=[
            ('total', 'Total'),
            ('partial', 'Partial')
        ],
        string='Payment amount type',
        default='total'
    )
    show_pay_button = fields.Boolean(
        string='Show Pay button',
        compute='_compute_show_pay_button',
        store=False
    )

    @api.multi
    def _compute_show_pay_button(self):
        id_need_check = int(
            self.env['ir.config_parameter'].sudo().get_param(
                'tpv_payment_mode_id_show_pay_button'
            )
        )
        for item in self:
            item.show_pay_button = False
            if item.proforma:
                if item.payment_mode_id:
                    if item.payment_mode_id.id == id_need_check:
                        item.show_pay_button = True
                        # check if completyly pay
                        transactions_amount = 0
                        for transaction_id in item.transaction_ids:
                            if transaction_id.state == 'done':
                                transactions_amount += transaction_id.amount
                        # check
                        if transactions_amount >= item.amount_total:
                            item.show_pay_button = False
            # override (url_return for payment form)
            if request:
                payment_ok_get = str(request.httprequest.args.get('payment_ok'))
                if payment_ok_get is not None:
                    if payment_ok_get == '1':
                        item.show_pay_button = False
