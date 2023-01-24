from odoo import models, fields, api
from odoo.exceptions import ValidationError
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
    garden_ares = fields.Integer(string="Garden Area")
    status = fields.Selection(string="Status", selection=[('N', 'New'), ('OR','Offer Received'), ('OA','Offer Accepted'),('S','Sold'),
                                    ('C','Canceled')],copy = False, default = "N")
    garden_orientation = fields.Selection(string="Garden Orientation", selection=[('N', 'North'), ('S','South'), ('E', 'East'), ('W', 'West')])
    active = fields.Boolean("Active?", default=True)
    type_id = fields.Many2one("property.type", ondelete='cascade')
    seller_id = fields.Many2one("res.users", default = lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", copy = False)
    tag_ids = fields.Many2many("property.tag")
    offer_ids = fields.One2many("property.offer", 'property_id')

    @api.constrains("garden_ares", "garden_orientation")
    def _check_if_there_is_a_garden(self):
        self.ensure_one()
        if not self.garden and (self.garden_ares or self.garden_orientation):
            raise ValidationError("There is not any garden so no garden area nor orientation")
        
        


class PropertyType(models.Model):
    _name =  "property.type"
    _description = "Type of properties"
    name = fields.Char(required=True)


class PropertyTag(models.Model):
    _name="property.tag"
    _description="Specific characteristics of the property"
    name = fields.Char(required=True)

class PropertyOffer(models.Model):
    _name="property.offer"
    _description="Buyers offers for certain property"

    price = fields.Float()
    status = fields.Selection(selection = [('A', 'Accepted'), ('R', 'Refused')], copy=False)
    partner_id=fields.Many2one('res.partner',required=True)
    property_id = fields.Many2one('estate.property',required=True)