# -*- coding: utf-8 -*-

from datetime import date
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class StatePropertyOffer(models.Model):
    _name = 'state.property.offer'
    _description = 'State property offer'

    values_status = [('accepted', 'Accepted'), ('refused', 'Refused')]

    price = fields.Float("Price")
    status = fields.Selection(selection=values_status, string="Status", copy=False)
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one(comodel_name="state_property.state_property", string="State property", required=True)
