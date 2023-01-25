# -*- coding: utf-8 -*-

from odoo import models, fields, api


class estate_account(models.Model):
    _name = 'estate_account.estate_account'
    _description = 'estate_account.estate_account'
    _inherit = 'estate_property.estate.property'

    name = fields.Char()
    description = fields.Text()

    