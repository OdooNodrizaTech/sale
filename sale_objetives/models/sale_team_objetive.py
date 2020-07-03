# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models

import logging
_logger = logging.getLogger(__name__)

class SaleTeamObjetive(models.Model):
    _name = 'sale.team.objetive'
    _description = 'Sale Team Objetive'
    
    team_id = fields.Many2one(
        comodel_name='crm.team',        
        string='Equipo',
    )
    date = fields.Date(        
        string='Fecha'
    )
    value = fields.Float(        
        string='Valor'
    )                            