# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models, _
from odoo.exceptions import Warning as UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def action_confirm(self):
        allow_action_confirm = True

        for item in self:
            if item.carrier_id and item.partner_shipping_id:
                if not item.partner_shipping_id.street:
                    allow_action_confirm = False
                    raise UserError(
                        _('It is necessary to define an address to send')
                    )
                elif not item.partner_shipping_id.city:
                    allow_action_confirm = False
                    raise UserError(
                        _('It is necessary to define a city / town to send')
                    )
                elif not item.partner_shipping_id.zip:
                    allow_action_confirm = False
                    raise UserError(
                        _('It is necessary to define a postal code to send')
                    )
                elif item.partner_shipping_id.country_id == 0:
                    allow_action_confirm = False
                    raise UserError(
                        _('It is necessary to define a country to send')
                    )
                elif item.partner_shipping_id.state_id == 0:
                    allow_action_confirm = False
                    raise UserError(
                        _('It is necessary to define a state to send')
                    )

        if allow_action_confirm:
            return super(SaleOrder, self).action_confirm()
