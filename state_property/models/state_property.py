# -*- coding: utf-8 -*-

from datetime import date
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class StateProperty(models.Model):
    _name = 'state_property.state_property'
    _description = 'State property'

    _sql_constraints = [
        ('unique_postcode', 'unique (postcode)', 'Postcode must be unique.'),
        ('check_expected_price', 'check (expected_price > 0)', 'Expected price must be non zero possitive number.')
    ]

    orientation = [('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')]

    name = fields.Char("Name", required=True)
    description = fields.Text("Description")
    postcode = fields.Char("Postcode")
    date_availability = fields.Date("Date availability")
    expected_price = fields.Float("Expected price", required=True)
    selling_price = fields.Float("Selling price")
    bedrooms = fields.Integer("Bedrooms")
    living_area = fields.Integer("Living area")
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Garage", default=False)
    garden = fields.Boolean("Garden", default=False)
    garden_area = fields.Integer("Garden area")
    garden_orientation = fields.Selection(selection=orientation, string="Garden orientation")
    # state_property_type = fields.Many2one("", related=)

    @api.constrains('date_availability')
    def _check_date_availability(self):
        for rec in self:
            if rec.date_availability and rec.date_availability < fields.Date.today():
                raise ValidationError(_("The entered date availability is not acceptable !"))


class StatePropertyType(models.Model):
    _name = 'state_property_type.state_property_type'
    _description = 'State property type'

    _sql_constraints = [
        ('unique_name', 'unique (name)', 'Name must be unique.')
    ]

    name = fields.Char("Name", required=True)
    # state_property = fields.One2many("StateProperty")
