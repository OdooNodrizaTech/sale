# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SaleUserObjetive(models.Model):
    _name = 'sale.user.objetive'
    _description = 'Sale User Objetive'
    
    user_id = fields.Many2one(
        comodel_name='res.users',        
        string='User',
    )
    date = fields.Date(        
        string='Date'
    )
    value = fields.Float(        
        string='Value'
    )                            