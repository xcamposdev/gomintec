# -*- coding: utf-8 -*-

import logging
import threading
from psycopg2 import sql
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, tools, SUPERUSER_ID
from odoo.tools.translate import _
from odoo.tools import email_re, email_split
from odoo.exceptions import UserError, AccessError
from odoo.addons.phone_validation.tools import phone_validation
from collections import OrderedDict, defaultdict

class Lead_custom(models.Model):
    _name = "crm.lead"
    _inherit = "crm.lead"
    
    x_file_number = fields.Char(string='Nº Expediente')
    x_execution_place_id = fields.Many2one("res.partner", string='Lugar de ejecución', copied=True, store=True)
    x_partner_execution_place_id = fields.Many2one("res.partner", string='Contacto', copied=True, store=True)
    x_project_manager_id = fields.Many2one("res.partner", string='Project manager', copied=True, store=True)
    x_planner_executor_id = fields.Many2one("res.partner", string='Proyectista', copied=True, store=True)
    x_file_manager_id = fields.Many2one("res.partner", string='Director de expediente', copied=True, store=True)
 