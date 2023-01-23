# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StatePropertyOffer(models.Model):
    _name = 'state.property.offer'
    _description = 'State property offer'
    _order = 'price desc'

    _sql_constraints = [
        ('check_price', 'check (price > 0)', 'An offer price must be strictly positive.')
    ]

    values_status = [('accepted', 'Accepted'), ('refused', 'Refused')]

    price = fields.Float("Price")
    status = fields.Selection(selection=values_status, string="Status", copy=False)
    validity = fields.Integer("Validity", default=7)
    date_deadline = fields.Date()
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one(comodel_name="state_property.state_property", string="State property", required=True)
