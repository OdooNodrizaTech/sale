[![Build Status](https://travis-ci.org/OdooNodrizaTech/sale.svg?branch=12.0)](https://travis-ci.org/OdooNodrizaTech/sale)

sale
=========
Módulos relacionados con Sale


Addons
----------------
nombre | version
--- | ---
[cashondelivery](cashondelivery/) | 12.0.1.0.0
[sale_order_confirm_bank_account_required](sale_order_confirm_bank_account_required/) | 12.0.1.0.0
[sale_order_confirm_mandate_required](sale_order_confirm_mandate_required/) | 12.0.1.0.0
[sale_order_confirm_partner_shipping_info_required](sale_order_confirm_partner_shipping_info_required/) | 12.0.1.0.0
[sale_order_confirm_payment_mode_id_required](sale_order_confirm_payment_mode_id_required/) | 12.0.1.0.0
[sale_order_confirm_payment_term_id_required](sale_order_confirm_payment_term_id_required/) | 12.0.1.0.0
[sale_order_line_price_unit_float](sale_order_line_price_unit_float/) | 12.0.1.0.0
[sale_order_link_tracker](sale_order_link_tracker/) | 12.0.1.0.0
[sale_order_picking_priority](sale_order_picking_priority/) | 12.0.1.0.0
[sale_order_pricelist_id_update_line_prices_button](sale_order_pricelist_id_update_line_prices_button/) | 12.0.1.0.0
[sale_order_template_arelux](sale_order_template_arelux/) | 12.0.1.0.0
[sale_order_template_child](sale_order_template_child/) | 12.0.1.0.0
[sale_orders_done_full_invoiced](sale_orders_done_full_invoiced/) | 12.0.1.0.0
[sale_orders_free_auto_invoiced](sale_orders_free_auto_invoiced/) | 12.0.1.0.0
[sale_orders_generate_invoice](sale_orders_generate_invoice/) | 12.0.1.0.0
[sale_orders_set_date_invoice](sale_orders_set_date_invoice/) | 12.0.1.0.0

## Addons no soportados

### sale_float_round
Actualmente no se observan 3 o + decimales en la BBDD por lo que probablemente esté resuelto este "extraño" problema que sucedía.

### sale_quote_template_child
Se ha renombrado a sale_order_template_child

### sale_orders_set_website_description
No es necesario usarlo en V12 porque el campo de website_description no existe en el sale_order

### website_quote_arelux
Se ha renombrado a sale_order_template_arelux
