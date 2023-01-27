from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError
from datetime import timedelta, date


class EstateProperty(models.Model):

    _name = "estate.property"
    _description = "Some description"
    _order ="id desc"

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
    state = fields.Selection(string="Status", selection=[('N', 'New'), ('OR','Offer Received'), ('OA','Offer Accepted'),('S','Sold'),
                                    ('C','Canceled')],copy = False, default = "N")
    garden_orientation = fields.Selection(string="Garden Orientation", selection=[('N', 'North'), ('S','South'), ('E', 'East'), ('W', 'West')])
    active = fields.Boolean("Active?", default=True)
    type_id = fields.Many2one("property.type", ondelete='cascade')
    seller_id = fields.Many2one("res.users", default = lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", copy = False)
    tag_ids = fields.Many2many("property.tag")
    offer_ids = fields.One2many("property.offer", 'property_id')
    total_area = fields.Float(compute="_get_total_area", readonly=True)
    best_offer = fields.Float(compute="_get_best_offer",readonly=True)

    _sql_constraints = [('check_expected_price', 'CHECK(expected_price>0 AND selling_price>0)','Price must be positive.')]

    @api.constrains("garden_ares", "garden_orientation")
    def _check_if_there_is_a_garden(self):
        self.ensure_one()
        if not self.garden and (self.garden_ares or self.garden_orientation):# If there are not records self.value=False if value is selection type
            raise ValidationError("There is not any garden so no garden area nor orientation")

    @api.depends('living_area', 'garden_ares')
    def _get_total_area(self):
        try:
            self.ensure_one()    
            self.total_area=self.living_area+self.garden_ares
        except ValidationError:
            return

    @api.depends('offer_ids')
    def _get_best_offer(self):
        try:
            self.best_offer = max(offer.price for offer in self.offer_ids)
        except ValueError:
            self.best_offer = 0

    @api.onchange('garden')
    def _set_defaults(self):
        if self.garden:
            self.garden_ares=10
            self.garden_orientation="N"
            return
            
        self.garden_ares=0
        self.garden_orientation=None   

    def cancel_property(self):
        if self.state == "S":
            raise UserError("A sold property can't be cancelled")
        self.state="C"
        return True

    def set_property_as_sold(self):
        if self.state == "C":
            raise UserError("Cancelled property can't be sold")
        self.state = "S"
        return True

    @api.onchange('expected_price')
    def _check_offers(self):
        limit_price = 90 * self.expected_price / 100
        for offer in self.offer_ids:
            if offer.price < limit_price and offer.status=='A':
                raise UserError('''The selling price must be at least 90% of expected price in order to accept any offer, 
                so first refuse the accepted offer.''')

        
   


class PropertyType(models.Model):
    _name =  "property.type"
    _description = "Type of properties"
    _order = "sequence,name"

    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property", 'type_id')
    offer_ids = fields.One2many("property.offer", 'property_type_id')
    offer_count = fields.Integer(compute="_count_offers", readonly=True)
    sequence = fields.Integer()

    _sql_constraints = [('check_name', 'UNIQUE(name)',f'Name already exists.')]

    @api.depends('offer_ids')
    def _count_offers(self):
        self.offer_count = len(self.offer_ids)

class PropertyTag(models.Model):
    _name="property.tag"
    _description="Specific characteristics of the property"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer()

    _sql_constraints = [('check_name', 'UNIQUE(name)',f'Name already exists.')]

class PropertyOffer(models.Model):
    _name="property.offer"
    _description="Buyers offers for certain property"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(selection = [('A', 'Accepted'), ('R', 'Refused')], copy=False)
    partner_id=fields.Many2one('res.partner',required=True)
    property_id = fields.Many2one('estate.property',required=True)
    validity = fields.Integer(default=7)
    property_type_id = fields.Many2one(related='property_id.type_id', store=True)
    date_deadline= fields.Date(compute="_get_deadline", inverse="_get_validity")

    _sql_constraints = [('check_price', 'CHECK(price>0)','Price must be positive.')]

    @api.depends('validity')
    def _get_deadline(self):
        for offer in self:
            offer.date_deadline =offer.create_date + timedelta(days=offer.validity) if offer.create_date else None


    def _get_validity(self):
        for offer in self:
            if  offer.date_deadline:
                cd = offer.create_date
                offer.validity = (offer.date_deadline  - date(cd.year,cd.month,cd.day)).days 

    def accept_offer(self):
        if self.search_count([('property_id.id','=',self.property_id.id), ('status','=', 'A')]):
            raise UserError('Only one offer can be accepted!')
        self.status='A'
        if self.price < 90 * self.property_id.expected_price/100:
            raise UserError('The selling price must be at least 90% of expected price in order to accept this offer.')
        self.property_id.selling_price = self.price
        self.property_id.buyer_id = self.partner_id
        return True
    
    def refuse_offer(self):
        self.status='R'
        return True
