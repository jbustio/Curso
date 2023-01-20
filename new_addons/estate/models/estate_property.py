from odoo import models, fields
class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'
    
    name = fields.Char('Name', required=True)
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
    garden_orientation = fields.Selection([
        ('north', 'North'),('south','South'),('east','East'),('west','West'),
    ], string='Garden Orientation')
    property_type_id = fields.Many2one('estate.property.type', string='Property Type')
    tag_ids = fields.Many2many('estate.property.tag', string='Tag')
    offer_ids = fields.Many2many('estate.property.offer', string='Offer')

class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type'

    name = fields.Char('Type', required=True)

class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate Property Tag'
    
    name = fields.Char('Tag', required=True)

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'

    price = fields.Float('price')
    status = fields.Selection([
        ('accepted', 'Accepted'),('refused','Refused')
    ], string='status')
    partner_id = fields.Many2one('res.partner', string='partner', required=True)
    property_id = fields.Many2one('estate.property', string='property',required=True)
    