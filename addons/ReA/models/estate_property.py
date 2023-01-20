from odoo import models, fields
from datetime import timedelta, datetime

class EstateProperty(models.Model):

    _name = "estate.property"
    _description = "Some description"

    name = fields.Char()
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=lambda self: fields.Datetime.now() + timedelta(days=54))
    expected_price = fields.Float()
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    fecades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_ares = fields.Integer()
    available = fields.Boolean(default = True)
    garden_orientation = fields.Selection(string="Garden Orientation", selection=[('N', 'North'), ('S','South'), ('E', 'East'), ('W', 'West')])
