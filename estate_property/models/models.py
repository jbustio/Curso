# -*- coding: utf-8 -*-

from odoo import models, fields, api


class estate_property(models.Model):
    _name = 'estate_property.estate_property'
    _description = 'estate_property.estate_property'

    name = fields.Char(required = True)
    description = fields.Text()
    postcode = fields.Char(compute="_value_pc", store=True)
    date_availabity = fields.Date()
    expected_price = fields.Float(required = True)
    selling_price = fields.Float()
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


    @api.depends('value')
    def _value_pc(self):
        for record in self:
            record.value2 = float(record.value) / 100
