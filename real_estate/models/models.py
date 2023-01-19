# -*- coding: utf-8 -*-

from odoo import models, fields, api


class RealEstatePropertyTag(models.Model):
    _name = 'real.estate.property.tag'
    _description = 'Real Estate Property Tag model class'

    _rec_name = 'name'
    _order = 'name ASC'

    name = fields.Char(
        string='Name',
        required=True,
    )


class RealEstatePropertyType(models.Model):
    _name = 'real.estate.property.type'
    _description = 'Real Estate Property Type model class'

    _rec_name = 'name'
    _order = 'name ASC'

    name = fields.Char(
        string='Name',
        required=True,
    )
    # real_state_property_ids = fields.One2many('real.estate.property', String="Real Estate Properties")


class RealEstateProperty(models.Model):
    _name = 'real.estate.property'
    _description = 'Real Estate Property model class'

    name = fields.Char(required=True, String="name")
    description = fields.Text(String="Description")
    postcode = fields.Text(String="Postcode")
    date_availability = fields.Date(String="Date Availability")
    expected_price = fields.Float(required=True)
    selling_price = fields.Float()
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])
    property_type_id = fields.Many2one('real.estate.property.type', string="Property Type")
    tag_ids = fields.Many2many('real.estate.property.tag', string="Property Tags")