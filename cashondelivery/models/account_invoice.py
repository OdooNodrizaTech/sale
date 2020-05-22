import logging
_logger = logging.getLogger(__name__)

from odoo import api, models, fields

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    total_cashondelivery = fields.Float(
        compute='_total_cashondelivery',
        store=False,
        string='Total contrareembolso pedido'
    )

    @api.one
    def _total_cashondelivery(self):
        if self.id != False and self.origin != '':
            sale_order_obj = self.env['sale.order'].search([('name', '=', self.origin)])
            self.total_cashondelivery = sale_order_obj.total_cashondelivery