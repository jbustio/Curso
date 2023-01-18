from odoo import fields, models, api


class ModelName(models.Model):
    _name = 'state.property'
    _description = 'Primer Modelo en Odoo'

    garden_orientation_choice=[
        ('North','North'),
        ('South','South'),
        ('East','East'),
        ('Weast','Weast')
    ]

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date()
    expected_price = fields.Float(digits=(32,32), required=True)
    selling_price = fields.Float(digits=(32,32))
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(garden_orientation_choice)
