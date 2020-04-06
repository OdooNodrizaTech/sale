# -*- coding: utf-8 -*-
import logging
_logger = logging.getLogger(__name__)

from openerp import api, models, fields
from openerp.exceptions import Warning
from datetime import datetime

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'
    
    @api.one    
    def action_auto_create(self):
        return True
        
    @api.one    
    def action_auto_open(self):
        return True                