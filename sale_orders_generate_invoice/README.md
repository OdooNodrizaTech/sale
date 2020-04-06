Define un cron para generar las facturas de clientes automáticamente de acuerdo a los pedidos de venta.

## Crones

### Sale Orders Generate Invoice

Frecuencia: 1 vez al día

Descripción: Revisa todos los ptos confirmados en estado "Pedido de venta" con importe > 0€, con modo de pago definido, que NO tenga desactivada la generación de facturas y cuyo "Estado de factura" sea "A facturar". Para cada uno de lo pedidos revisa las líneas del pedido de venta, y de aquellos que se facturen segun cantidades pedidas se factura las uds del pedido de venta, y para los que se facturen según cantidades enviadas (la mayoría de los productos deberían ser así) se revisa si el AV correspondiente está en estado "Hecho" para así proceder a facturar ese pedido según corresponda (uds enviadas).
