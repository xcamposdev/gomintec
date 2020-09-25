# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from functools import partial
from itertools import groupby

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.tools.misc import formatLang, get_lang
from odoo.osv import expression
from odoo.tools import float_is_zero, float_compare

class SaleOrderLine_custom(models.Model):
    _name = "sale.order.line"
    _inherit = "sale.order.line"
    
    x_margen_k = fields.Float('Margen', required=True, default=1.0)
    x_transporte = fields.Float('Transporte', required=True, default=1.0)
    x_money_change = fields.Float('Cambio Moneda', required=True, default=1.0)
    x_descuento_compra = fields.Float('Descuento compra', required=True, default=0.0)
    x_coste_unitario = fields.Float('Coste unitario', readonly=True)
    
    @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id', 'x_margen_k', 'x_descuento_compra', 'x_money_change', 'x_transporte')
    def _compute_amount(self):
        """
        Compute the amounts of the SO line.
        """
        for line in self:
            price = ((line.purchase_price-line.purchase_price*(line.x_descuento_compra/100.0))*line.x_money_change*line.x_transporte)*line.x_margen_k * (1 - (line.discount or 0.0) / 100.0) #custom           
            price = round(price,2)
            taxes = line.tax_id.compute_all(price, line.order_id.currency_id, line.product_uom_qty, product=line.product_id, partner=line.order_id.partner_shipping_id)
            line.update({
                'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
                
            })
