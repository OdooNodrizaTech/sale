# -*- coding: utf-8 -*-
from odoo import api, models, fields
from odoo.exceptions import Warning

import logging
_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def action_confirm(self):
        allow_action_confirm = True
        for item in self:
            if item.amount_total>0 and item.payment_mode_id.id>0:
                if item.payment_mode_id.payment_method_id.id>0:
                    if item.payment_mode_id.payment_method_id.mandate_required==True:
                        #partner_id_check
                        partner_id_check = item.partner_invoice_id.id
                        if item.partner_invoice_id.parent_id.id > 0:
                            partner_id_check = item.partner_invoice_id.parent_id.id
                        #account_banking_mandate_ids
                        account_banking_mandate_ids = self.env['account.banking.mandate'].search([('partner_bank_id.partner_id', '=', partner_id_check)])
                        if len(account_banking_mandate_ids) == 0:
                            allow_action_confirm = False
                            raise Warning("No se puede confirmar la venta porque no hay un mandato bancario creado para la direccion de facturacion seleccionada")

        if allow_action_confirm == True:
            return super(SaleOrder, self).action_confirm()