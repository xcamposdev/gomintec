# -*- coding: utf-8 -*-

import logging
from odoo import api, fields, models, exceptions, _
from odoo.exceptions import AccessError, UserError, ValidationError

_logger = logging.getLogger(__name__)

class sale_order_line_custom_0(models.Model):

    _inherit = 'sale.order.line'

    x_mostrar_seccion = fields.Text(compute='get_description')

    def get_description(self):
        for rec in self:
            if(rec.display_type):
                rec.x_mostrar_seccion = rec.name
            else:
                rec.x_mostrar_seccion = ""
