# -*- coding: utf-8 -*-

import logging
from odoo import api, fields, models, exceptions, _
from odoo.exceptions import AccessError, UserError, ValidationError

_logger = logging.getLogger(__name__)

class sale_order_line_custom_0(models.Model):

    _inherit = 'sale.order.line'

    #name = fields.Text(string='Description', required=True)
    x_mostrar_seccion = fields.Text()

    @api.onchange('x_mostrar_seccion')
    def _onchange_x_mostrar_seccion(self):
        test = "te"
        if(self.x_mostrar_seccion):
            self.name = self.x_mostrar_seccion

    @api.onchange('name')
    def _onchange_name_0(self):
        test = "te"
        if(self.display_type!=False):
            self.x_mostrar_seccion = self.name