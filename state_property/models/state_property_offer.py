# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StatePropertyOffer(models.Model):
    _name = 'state.property.offer'
    _description = 'State property offer'
    _order = 'price desc'

    _sql_constraints = [
        ('check_price', 'CHECK (price < 0)', 'An offer price must be strictly positive.')
    ]

    values_status = [('accepted', 'Accepted'), ('refused', 'Refused')]

    price = fields.Float("Price")
    status = fields.Selection(selection=values_status, string="Status", copy=False)
    validity = fields.Integer("Validity", default=7)
    date_deadline = fields.Date()
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one(comodel_name="state_property.state_property", string="State property", required=True)

    # Actions Buttons
    def action_accept(self):
        for record in self:
            if not record.status:
                record.status = 'accepted'
                record.property_id.selling_price = record.price
        return True

    def action_refuse(self):
        for record in self:
            if not record.status:
                record.status = 'refused'
        return True
