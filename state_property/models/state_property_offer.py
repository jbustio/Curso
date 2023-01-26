# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date
from dateutil.relativedelta import relativedelta


class StatePropertyOffer(models.Model):
    _name = 'state.property.offer'
    _description = 'State property offer'
    _order = 'price desc'

    _sql_constraints = [
        ('check_price', 'CHECK (price > 0)', 'An offer price must be strictly positive.')
    ]

    values_status = [('accepted', 'Accepted'), ('refused', 'Refused')]

    price = fields.Float("Price", required=True)
    status = fields.Selection(selection=values_status, string="Status", copy=False, readonly=True)  # default = False
    validity = fields.Integer("Validity (days)", default=7)
    date_deadline = fields.Date("Date deadline", compute="_compute_date_dead_line", inverse="inverse_compute_date_dead_line")
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one(comodel_name="state_property.state_property", string="State property", required=True)

    # Method _computed
    @api.depends('create_date', 'validity')
    def _compute_date_dead_line(self):
        for record in self:
            var_date = record.create_date.date() if record.create_date else date.today()
            record.date_deadline = var_date + relativedelta(days=record.validity)

    def inverse_compute_date_dead_line(self):
        for record in self:
            var_date = record.create_date.date() if record.create_date else date.today()
            record.validity = (record.date_deadline - var_date).days

    # Actions Buttons
    def action_accept(self):
        for record in self:
            return record.write({
                'status': 'accepted',
                'property_id.selling_price': 'price',
                'property_id.buyer': 'partner_id'
            })

    def action_refuse(self):
        for record in self:
            return record.write({
                'status': 'refused'
            })
