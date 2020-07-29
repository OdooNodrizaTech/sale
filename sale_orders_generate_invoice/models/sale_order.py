# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import logging
from odoo import api, models, _
from datetime import datetime

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def action_account_invoice_not_create_partner_without_vat(self):
        return True

    @api.multi
    def allow_generate_invoice(self):
        # check
        allow_generate_invoice = False
        need_delivery_something = False
        for item in self:
            if item.invoice_status == 'to invoice':
                total_qty_to_invoice = 0

                for order_line in item.order_line:
                    if order_line.product_id.invoice_policy == 'order':
                        total_qty_to_invoice = \
                            total_qty_to_invoice + order_line.product_uom_qty
                    else:
                        total_qty_to_invoice = \
                            total_qty_to_invoice + order_line.qty_delivered
                        need_delivery_something = True

                if total_qty_to_invoice > 0:
                    allow_generate_invoice = False

                    if need_delivery_something:
                        stock_picking_date_done = False
                        all_stock_picking_done = True
                        # picking_ids
                        for picking_id in item.picking_ids:
                            if picking_id.picking_type_id.code == 'outgoing':
                                if picking_id.state == 'done':
                                    stock_picking_date_done = picking_id.date_done
                                else:
                                    all_stock_picking_done = False
                        # operations
                        if all_stock_picking_done and stock_picking_date_done:
                            allow_generate_invoice = True
                    else:
                        allow_generate_invoice = True
                    # check nif
                    if allow_generate_invoice:
                        if not item.partner_invoice_id.vat:
                            allow_generate_invoice = False
                            item.action_account_invoice_not_create_partner_without_vat()
                            _logger.info(
                                _('The order %s cannot be invoiced because the client '
                                  'does NOT have a CIF') % item.name
                            )
        # return
        return allow_generate_invoice

    @api.model
    def cron_action_orders_generate_invoice(self):
        current_date = datetime.today()
        allow_generate_invoices = True

        if current_date.day == 31 and current_date.month == 12:
            allow_generate_invoices = False

        if current_date.day == 1 and current_date.month == 1:
            allow_generate_invoices = False

        if allow_generate_invoices:
            items = self.env['sale.order'].search(
                [
                    ('state', '=', 'sale'),
                    ('amount_total', '>', 0),
                    ('payment_mode_id', '!=', False),
                    ('invoice_status', '=', 'to invoice'),
                    ('disable_autogenerate_create_invoice', '=', False)
                ]
            )
            if items:
                # group_by_partner_id
                ids_by_partner_id = {}
                for item in items:
                    # check
                    allow_generate_invoice = item.allow_generate_invoice()[0]
                    # add if need
                    if allow_generate_invoice:
                        if item.partner_invoice_id.id not in ids_by_partner_id:
                            ids_by_partner_id[item.partner_invoice_id.id] = []
                        # add_sale_order_ids
                        ids_by_partner_id[item.partner_invoice_id.id].append(item.id)

                if len(ids_by_partner_id) > 0:
                    for partner_id in ids_by_partner_id:
                        ids = ids_by_partner_id[partner_id]
                        items = self.env['sale.order'].search(
                            [
                                ('id', 'in', ids)
                            ]
                        )
                        # action_invoice_create
                        try:
                            res = items.action_invoice_create()
                            # sale_order_ids
                            for item in items:
                                item.state = 'done'
                            # invoice_ids
                            invoice_id = self.env['account.invoice'].browse(res[0])
                            # action_auto_create
                            invoice_id.action_auto_create()
                            # operations
                            if invoice_id.amount_total > 0:
                                invoice_id.action_invoice_open()
                                # action_auto_open
                                invoice_id.action_auto_open()
                                # send mail
                                invoice_id.cron_account_invoice_auto_send_mail_item()
                        except:
                            _logger.info(_('An error occurred while generating '
                                           'the invoice for the orders'))
                            for item in items:
                                _logger.info(item.name)
