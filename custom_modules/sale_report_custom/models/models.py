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
            
class SaleOrderOption_custom(models.Model):
    _name = "sale.order.option"
    _inherit = "sale.order.option"
    
    x_margen_k = fields.Float('Margen', required=True, default=1.0)
    x_transporte = fields.Float('Transporte', required=True, default=1.0)
    x_money_change = fields.Float('Cambio Moneda', required=True, default=1.0)
    x_descuento_compra = fields.Float('Descuento compra', required=True, default=0.0)
    x_coste_unitario = fields.Float('Coste unitario', readonly=True, compute="coste_unitario")
    x_coste_total = fields.Float('Coste total', readonly=True, compute="coste_total")
    x_precio_venta_unitario = fields.Float('Precio venta unitario', readonly=True, compute="precio_venta_unitario")
    x_coste = fields.Float('Coste')
    
    @api.depends('x_transporte', 'x_money_change', 'x_descuento_compra')
    def coste_unitario(self):
        for i in self:
            i.x_coste_unitario = i.x_coste * (1.0-(i.x_descuento_compra/100.0)) * i.x_money_change * i.x_transporte
    
    @api.depends('x_transporte', 'x_money_change', 'x_descuento_compra') 
    def coste_total(self):
        for i in self:
            i.x_coste_total = i.x_coste_unitario * i.quantity
    
    @api.depends('x_transporte', 'x_money_change', 'x_descuento_compra', 'x_margen_k') 
    def precio_venta_unitario(self):
        for i in self:
            i.x_precio_venta_unitario = i.x_margen_k * i.x_coste_unitario
    
    @api.onchange('product_id', 'uom_id')
    def _onchange_product_id(self):
        if not self.product_id:
            return
        product = self.product_id.with_context(lang=self.order_id.partner_id.lang)
        self.name = product.get_product_multiline_description_sale()
        self.uom_id = self.uom_id or product.uom_id
        domain = {'uom_id': [('category_id', '=', self.product_id.uom_id.category_id.id)]}
        # To compute the dicount a so line is created in cache
        values = self._get_values_to_add_to_order()
        new_sol = self.env['sale.order.line'].new(values)
        new_sol._onchange_discount()
        self.discount = new_sol.discount
        self.price_unit = new_sol._get_display_price(product)
        self.x_coste = self.product_id.standard_price
        self.x_coste_total = self.product_id.standard_price
        self.x_coste_unitario = self.product_id.standard_price
        self.x_precio_venta_unitario = self.product_id.standard_price
        return {'domain': domain}
