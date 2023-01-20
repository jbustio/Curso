from odoo import fields, models
from dateutil.relativedelta import relativedelta


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Real Estate Property'
    _order = 'name ASC'

    name = fields.Char(default=lambda self: 'New Real Estate', required=True)
    tag_ids = fields.Many2many('estate.property.tag')
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        default=lambda self: fields.datetime.now() + relativedelta(months=2),
        copy=False, string="Available from")
    expected_price = fields.Float(required=True)
    selling_price = fields.Float()
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    property_type_id = fields.Many2one(
        "estate.property.type", string="Property Type")
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[('north', 'North'), ('south', 'South'),
                   ('east', 'East'), ('west', 'West'),],
    )
    salesperson_id = fields.Many2one(
        'res.users', string='Salesperson', index=True, tracking=True, default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', string="Buyer", copy=False)
    offer_ids = fields.One2many('estate.property.offer', 'property_id')


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'PropertyType'

    _rec_name = 'name'
    _order = 'name ASC'

    name = fields.Char(
        string='Name',
        required=True,
    )
    real_estate = fields.One2many(
        "estate.property", "property_type_id", string="Real Estates")


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'PropertyTag'

    _rec_name = 'name'
    _order = 'name ASC'

    name = fields.Char(
        string='Name',
        required=True,
    )


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'EstatePropertyOffer'

    price = fields.Float()
    status = fields.Selection(
        selection=[('accepted', 'Accepted'), ('refuse', 'Refuse'),], copy=False)
    partner_id = fields.Many2one('res.partner', string="Partner",
                                 required=True
                                 )
    property_id = fields.Many2one('estate.property',
                                  required=True
                                  )
