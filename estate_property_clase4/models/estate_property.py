from odoo import models, fields, api


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Mi Estate Property'
    _sql_constraints = [
        ('has_bedrooms', 'CHECK(bedrooms >= 0)', "Enter a bedrooms"),
        ('has_living_area', 'CHECK(living_area >= 0)', "Enter a living area"),
        ('has_expected_price', 'CHECK(expected_price >= 0)', "Enter a price"),
        ('has_selling_price', 'CHECK(selling_price >= 0)', "Enter a sell price"),
    ]
    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date()
    expected_price = fields.Float(required=True)
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

    property_type = fields.Many2one('real.estate.property.type', String="Property Types")
    taxes_ids = fields.Many2many('estate.property.taxes', string="Taxes")
    offer_ids = fields.One2many('estate.property.offer', string="Property Offers", inverse_name='property_id')
    buyer_id = fields.Many2one('res.partner', string="Buyer")
    salesman_id = fields.Many2one('res.users', string="Salesman", default=lambda self: self.env.user)


class RealEstatePropertyType(models.Model):
    _name = 'real.estate.property.type'
    _description = 'Mi real Description'

    name = fields.Char(required=True)
    property_type_ids = fields.One2many('estate.property',
                                        'property_type',
                                        string="Property Type")


class EstatePropertyTaxes(models.Model):
    _name = 'estate.property.taxes'
    _description = 'Mi real Description'

    name = fields.Char(required=True)


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer model class'

    price = fields.Float()
    status = fields.Selection(selection=[("accepted", "Accepted"), ('refused', "Refused")], copy=False)
    partner_id = fields.Many2one('res.partner', string="Real Estate Partner")
    property_id = fields.Many2one('estate.property', string="Estate Property")
