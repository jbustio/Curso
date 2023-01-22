# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero
from datetime import date
from dateutil.relativedelta import relativedelta


class StateProperty(models.Model):
    _name = 'state_property.state_property'
    _description = 'State property'

    _sql_constraints = [
        ('unique_postcode', 'unique (postcode)', 'Postcode must be unique.'),
        ('check_expected_price', 'check (expected_price > 0)', 'Expected price must be non zero possitive number.')
    ]

    values_orientation = [('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')]
    values_state = [('new', 'New'), ('offer_received', 'Offer received'), ('offer_accepted', 'Offer accepted'), ('sold', 'Sold'), ('canceled', 'Canceled')]

    name = fields.Char("Name", required=True)
    description = fields.Text("Description")
    postcode = fields.Char("Postcode")
    date_availability = fields.Date("Date availability", copy=False, default=lambda x: date.today() + relativedelta(months=3))
    expected_price = fields.Float("Expected price", required=True)
    selling_price = fields.Float("Selling price", readonly=True, copy=False)
    bedrooms = fields.Integer("Bedrooms", default=2)
    living_area = fields.Integer("Living area")
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Garage", default=False)
    garden = fields.Boolean("Garden", default=False)
    garden_area = fields.Integer("Garden area")
    garden_orientation = fields.Selection(selection=values_orientation, string="Garden orientation")
    property_type_id = fields.Many2one("state.property.type", string="State property type", required=True)
    tag_ids = fields.Many2many("state.property.tag", string='Tags')
    active = fields.Boolean("Active", default=True)
    state = fields.Selection(selection=values_state, string="State", required=True, copy=False, default=values_state[0][0])

    @api.constrains('date_availability')
    def _check_date_availability(self):
        for rec in self:
            if rec.date_availability and rec.date_availability < fields.Date.today():
                raise ValidationError(_("The entered date availability is not acceptable !"))


class StatePropertyType(models.Model):
    _name = 'state.property.type'
    _description = 'State property type'

    _sql_constraints = [
        ('unique_name', 'unique (name)', 'Name must be unique.')
    ]

    name = fields.Char("Name", required=True)


class StatePropertyTag(models.Model):
    _name = 'state.property.tag'
    _description = 'State property type'

    _sql_constraints = [
        ('unique_name', 'unique (name)', 'Name must be unique.')
    ]

    name = fields.Char("Name", required=True)
    # state_property = fields.One2many("StateProperty")
