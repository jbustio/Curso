# -*- coding: utf-8 -*-

from odoo import models, fields, api

print('==========================================IMPORTED==========================================')

class estate_property(models.Model):
    _name = 'estate_property.estate.property'
    _description = 'estate_property.estate.property'

    name = fields.Char(required = True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy = False)
    expected_price = fields.Float(required = True)
    selling_price = fields.Float(readonly = True)
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden area')
    garden_orientation = fields.Selection([
        ('North', 'North'),
        ('South', 'South'),
        ('East', 'East'),
        ('West', 'West'),
    ], string='Garden orientation')
    active = fields.Boolean(default = True)
    state = fields.Selection([
        ('New', 'New'),
        ('Offer Received', 'Offer Received'), 
        ('Offer Accepted', 'Offer Accepted'), 
        ('Sold', 'Sold'),
        ('Canceled', 'Canceled')
    ])

    @api.depends('value')
    def _value_pc(self):
        for record in self:
            record.value2 = float(record.value) / 100
