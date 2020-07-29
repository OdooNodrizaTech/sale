# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SaleTeamObjetive(models.Model):
    _name = 'sale.team.objetive'
    _description = 'Sale Team Objetive'
    
    team_id = fields.Many2one(
        comodel_name='crm.team',
        string='Team'
    )
    date = fields.Date(
        string='Date'
    )
    value = fields.Float(
        string='Value'
    )
