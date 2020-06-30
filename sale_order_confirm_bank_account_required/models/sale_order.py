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
                    if item.payment_mode_id.payment_method_id.bank_account_required==True:
                        #partner_id_check
                        partner_id_check = item.partner_invoice_id.id
                        if item.partner_invoice_id.parent_id.id > 0:
                            partner_id_check = item.partner_invoice_id.parent_id.id
                        #res_partner_bank_ids
                        res_partner_bank_ids = self.env['res.partner.bank'].search([('partner_id', '=', partner_id_check)])
                        if len(res_partner_bank_ids) == 0:
                            allow_action_confirm = False
                            raise Warning("No se puede confirmar la venta porque no hay una cuenta creada para la direccion de facturacion seleccionada")

        if allow_action_confirm == True:
            return super(SaleOrder, self).action_confirm()