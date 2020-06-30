# -*- coding: utf-8 -*-
import logging
_logger = logging.getLogger(__name__)

from odoo import api, models, fields
from odoo.exceptions import Warning

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    opportunity_id = fields.Many2one(
        comodel_name='crm.lead', 
        string='Opportunity', 
        domain="[('type', '=', 'opportunity')]", 
        required=True
    )
    show_total = fields.Boolean( 
        string='Mostrar total'
    )
    proforma = fields.Boolean( 
        string='Proforma'
    )        
    date_order_management = fields.Datetime(
        string='Fecha gestion', 
        readonly=True
    )
    date_order_send_mail = fields.Datetime(
        string='Fecha envio email', 
        readonly=True
    )        
    disable_autogenerate_create_invoice = fields.Boolean( 
        string='Desactivar auto facturar'
    )    
    partner_id_email = fields.Char(
        compute='_partner_id_email',
        store=False,
        string='Email'
    )
    partner_id_phone = fields.Char(
        compute='_partner_id_phone',
        store=False,
        string='Telefono'
    )
    partner_id_mobile = fields.Char(
        compute='_partner_id_mobile',
        store=False,
        string='Movil'
    )
    partner_id_state_id = fields.Many2one(
        comodel_name='res.country.state',
        compute='_get_partner_id_state_id',
        store=False,
        string='Provincia'
    )
    
    @api.onchange('partner_id')
    def onchange_partner_id_override(self):
        if self.partner_id.id>0:
            self.payment_mode_id = self.partner_id.customer_payment_mode_id.id or False
            #partner_shipping_id
            res_partner_ids = self.env['res.partner'].search(
                [
                    ('parent_id', '=', self.partner_id.id),
                    ('active', '=', True), 
                    ('type', '=', 'delivery')
                 ]
            )
            if len(res_partner_ids)>1:
                self.partner_shipping_id = 0
            elif len(res_partner_ids)==1:
                res_partner_id = res_partner_ids[0]
                self.partner_shipping_id = res_partner_id.id                                
    
    @api.model
    def fix_copy_custom_field_opportunity_id(self):
        if self.id>0:
            if self.opportunity_id.id>0:
                #user_id
                if self.opportunity_id.user_id.id>0 and self.opportunity_id.user_id.id!=self.user_id.id:
                    self.user_id = self.opportunity_id.user_id.id
                #team_id                    
                if self.opportunity_id.team_id.id>0 and self.opportunity_id.team_id.id!=self.team_id.id:
                    self.team_id = self.opportunity_id.team_id.id                                                              
    
    @api.model
    def create(self, values):            
        return_val = super(SaleOrder, self).create(values)            
        
        if return_val.user_id.id!=False and return_val.partner_id.user_id.id!=False and self.user_id.id!=return_val.partner_id.user_id.id:
            return_val.user_id = return_val.partner_id.user_id.id                        
        
        if return_val.user_id.id==6:
            return_val.user_id = 0
        
        return_val.fix_copy_custom_field_opportunity_id()#Fix copy fields opportunity
                        
        return return_val                                
    
    @api.multi
    def write(self, vals):
        #date_order_management
        if vals.get('state')=='sent' and 'date_order_management' not in vals:
            vals['date_order_management'] = fields.datetime.now()                            
                                        
        return_object = super(SaleOrder, self).write(vals)
    
        if self.user_id.id!=False:        
            for message_follower_id in self.message_follower_ids:
                if message_follower_id.partner_id.user_ids!=False:
                    for user_id in message_follower_id.partner_id.user_ids:
                        if user_id.id!=self.user_id.id:
                            self.env.cr.execute("DELETE FROM  mail_followers WHERE id = "+str(message_follower_id.id))                            
                                                            
        return return_object                    
    
    @api.one        
    def _get_partner_id_state_id(self):
        for sale_order_obj in self:
            sale_order_obj.partner_id_state_id = sale_order_obj.partner_id.state_id.id
    
    @api.one        
    def _partner_id_email(self):
        for sale_order_obj in self:
            sale_order_obj.partner_id_email = sale_order_obj.partner_id.email
            
    @api.one        
    def _partner_id_phone(self):
        for sale_order_obj in self:
            sale_order_obj.partner_id_phone = sale_order_obj.partner_id.phone
            
    @api.one        
    def _partner_id_mobile(self):
        for sale_order_obj in self:
            sale_order_obj.partner_id_mobile = sale_order_obj.partner_id.mobile                                                  
    
    @api.onchange('user_id')
    def change_user_id(self):                    
        if self.user_id.id>0:
            if self.user_id.sale_team_id.id>0:
                self.team_id = self.user_id.sale_team_id.id
                                                        
    @api.onchange('template_id')
    def change_template_id(self):
        if self.template_id.id>0:
            if self.template_id.delivery_carrier_id.id>0:
                self.carrier_id = self.template_id.delivery_carrier_id
            else:
                self.carrier_id = False                    
    
    @api.multi
    def action_confirm(self):
        allow_action_confirm = True
        
        if self.amount_total>0:    
            if self.carrier_id.id>0 and self.partner_shipping_id.id>0:
                if self.carrier_id.id>0 and self.partner_shipping_id.id>0 and self.partner_shipping_id.street==False:
                    allow_action_confirm = False
                    raise Warning("Es necesario definir una direccion para realizar el envio.\n")                
                elif self.carrier_id.id>0 and self.partner_shipping_id.id>0 and self.partner_shipping_id.city==False:
                    allow_action_confirm = False
                    raise Warning("Es necesario definir una ciudad/poblacion para realizar el envio.\n")                
                elif self.carrier_id.id>0 and self.partner_shipping_id.id>0 and self.partner_shipping_id.zip==False:
                    allow_action_confirm = False
                    raise Warning("Es necesario definir una codigo postal para realizar el envio.\n")                
                elif self.carrier_id.id>0 and self.partner_shipping_id.id>0 and self.partner_shipping_id.country_id==0:
                    allow_action_confirm = False
                    raise Warning("Es necesario definir una pais para realizar el envio.\n")                
                elif self.carrier_id.id>0 and self.partner_shipping_id.id>0 and self.partner_shipping_id.state_id==0:
                    allow_action_confirm = False
                    raise Warning("Es necesario definir una provincia para realizar el envio.\n")
                                                                                                                         
        if allow_action_confirm==True:
            return super(SaleOrder, self).action_confirm()        
    
    @api.multi
    def action_confirm(self):
        allow_confirm = True
        #check
        for obj in self:            
            if obj.carrier_id.id>0 and obj.partner_shipping_id.id>0:
                if obj.partner_shipping_id.street==False:
                    allow_confirm = False
                    raise Warning("Es necesario definir una direccion para realizar el envio.\n")                
                elif obj.partner_shipping_id.city==False:
                    allow_confirm = False
                    raise Warning("Es necesario definir una ciudad/poblacion para realizar el envio.\n")                
                elif obj.partner_shipping_id.zip==False:
                    allow_confirm = False
                    raise Warning("Es necesario definir una codigo postal para realizar el envio.\n")                
                elif obj.partner_shipping_id.country_id.id==0:
                    allow_confirm = False
                    raise Warning("Es necesario definir una pais para realizar el envio.\n")                
                elif obj.partner_shipping_id.state_id.id==0:
                    allow_confirm = False
                    raise Warning("Es necesario definir una provincia para realizar el envio.\n")            
        #allow_confirm
        if allow_confirm==True:
            return super(SaleOrder, self).action_confirm()                                                                                                