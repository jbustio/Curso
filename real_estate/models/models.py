# -*- coding: utf-8 -*-

from odoo import models, fields, api


class RealEstateProperty(models.Model):
    _name = 'real.estate.property'
    _description = 'Real Estate Property model class'

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Text()
    date_availability = fields.Date()
    expected_price = fields.Float(required=True)
    selling_price = fields.Float()
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])
