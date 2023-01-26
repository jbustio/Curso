# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StateAccount(models.Model):
    _inherit = ['state_property.state_property']

    def action_sold(self):
        return super().action_sold()
