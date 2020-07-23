# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'
                        
    date_invoice = fields.Date(
        string='Invoice date',
    )    
    
    @api.model    
    def cron_sale_orders_set_date_invoice(self):                
        sale_order_ids = self.env['sale.order'].search(
            [
                ('date_invoice', '=', False), 
                ('invoice_status', '=', 'invoiced'),
                ('state', 'in', ('sale', 'done')),
                ('amount_untaxed', '>', 0)
             ]
        )
        if sale_order_ids:
            for sale_order_id in sale_order_ids:
                date_invoice = False
                for invoice_id in sale_order_id.invoice_ids:
                    if invoice_id.type == 'out_invoice':
                        if invoice_id.date_invoice and date_invoice == False:
                            date_invoice = invoice_id.date_invoice
                # date_invoice
                if date_invoice:
                    sale_order_id.date_invoice = date_invoice                    