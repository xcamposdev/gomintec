# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from itertools import groupby

from odoo import api, fields, models, exceptions
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.tools import float_is_zero, float_compare

import zipfile
from datetime import datetime
from io import BytesIO


class SaleOrderCustom0(models.Model):

    _name = 'sale.order'
    _inherit = 'sale.order'

    def btn_catalogo_esp(self):
        product_id = []
        for line in self.order_line:
            if(line.product_id):
                product_id.append(line.product_id.id)
        url = '/web/binary/download_document?product_ids=%s&type=ficha_ESP' % product_id
        return {
            'type': 'ir.actions.act_url',
            'url': url,
            'target': 'new',
        }

    def btn_catalogo_en(self):
        product_id = []
        for line in self.order_line:
            if(line.product_id):
                product_id.append(line.product_id.id)
        url = '/web/binary/download_document?product_ids=%s&type=ficha_EN' % product_id
        return {
            'type': 'ir.actions.act_url',
            'url': url,
            'target': 'new',
        }

    def btn_certificado(self):
        product_id = []
        for line in self.order_line:
            if(line.product_id):
                product_id.append(line.product_id.id)
        url = '/web/binary/download_document?product_ids=%s&type=Cert' % product_id
        return {
            'type': 'ir.actions.act_url',
            'url': url,
            'target': 'new',
        }

  