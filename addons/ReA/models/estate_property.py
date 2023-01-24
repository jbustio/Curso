from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import timedelta, date

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
    total_area = fields.Float(compute="get_total_area", readonly=True)
    best_offer = fields.Float(compute="get_best_offer",readonly=True)

    @api.constrains("garden_ares", "garden_orientation")
    def _check_if_there_is_a_garden(self):
        self.ensure_one()
        if not self.garden and (self.garden_ares or self.garden_orientation):# If there are not records self.value=False if value is selection type
            raise ValidationError("There is not any garden so no garden area nor orientation")

    @api.depends('living_area', 'garden_ares')
    def get_total_area(self):
        try:
            self.ensure_one()    
            self.total_area=self.living_area+self.garden_ares
        except ValidationError:
            return

    @api.depends('offer_ids')
    def get_best_offer(self):
        try:
            self.best_offer = max(offer.price for offer in self.offer_ids)
        except ValueError:
            self.best_offer = 0

    @api.onchange('garden')
    def set_defaults(self):
        if self.garden:
            self.garden_ares=10
            self.garden_orientation="N"
            return
            
        self.garden_ares=0
        self.garden_orientation=None       
        


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
    validity = fields.Integer(default=7)
    date_deadline= fields.Date(compute="get_deadline", inverse="get_validity")

    @api.depends('validity')
    def get_deadline(self):
        for offer in self:
            offer.date_deadline =offer.create_date + timedelta(days=offer.validity) if offer.create_date else None

    def get_validity(self):
        for offer in self:
            if  offer.date_deadline:
                cd = offer.create_date
                offer.validity = (offer.date_deadline  - date(cd.year,cd.month,cd.day)).days 
