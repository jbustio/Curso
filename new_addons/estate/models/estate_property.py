from odoo import models, fields
class EstateProperty(models.Model):
    _name = 'EstateProperty'
    _description = 'Estate Property'
    
    name = fields.Char('Title', required=True)
    description = fields.Text('Description')
    postcode = fields.Char()
    date_availability = fields.Date()
    expected_price = fields.Float(required=True)
    selling_price = fields.Float()
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection['North', 'South', 'East', 'West']