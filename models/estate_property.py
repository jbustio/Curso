from odoo import api, fields, models
from dateutil.relativedelta import relativedelta
from datetime import datetime

from odoo.exceptions import UserError, ValidationError


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Real Estate Property'
    _order = "id desc"

    name = fields.Char(default=lambda self: 'New Real Estate', required=True)
    state = fields.Selection(required=True, default="new", copy=False,
                             selection=[('new', 'New'), ('offer_receive', 'Offer Received'), (
                                 'offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('canceled', 'Canceled'),])
    tag_ids = fields.Many2many('estate.property.tag')
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Datetime(
        default=lambda self: fields.datetime.today() + relativedelta(months=3),
        copy=False, string="Available from")
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(
        readonly=True, copy=False
    )

    bedrooms = fields.Integer(default=2)
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
    total_area = fields.Float(compute="_compute_total_area")
    active = fields.Boolean(default=1)
    best_price = fields.Float(compute='_compute_best_price')

    @api.depends('offer_ids')
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                print("!!!!!", record.offer_ids)
                bp = max(record.offer_ids.mapped('price'))
                record.best_price = bp
            else:
                print("!!! no hay offers")
                record.best_price = 0

    @api.depends("garden_area", "living_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = None
            self.garden_orientation = None

    def action_cancel(self):
        for record in self:
            if record.state not in ['sold', 'canceled']:
                record.state = 'canceled'
                return True

            raise UserError(f"A {record.state} property can not be cancel")

    def action_sell(self):
        for record in self:
            if record.state not in ['sold', 'canceled']:
                record.state = 'sold'
                return True
            raise UserError(f"A {record.state} property can not be sold")


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'PropertyType'

    _rec_name = 'name'
    _order = 'name ASC'

    name = fields.Char(
        string='Name',
        required=True,
    )

    property_ids = fields.One2many(
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
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        selection=[('accepted', 'Accepted'), ('refuse', 'Refuse'),], copy=False)
    partner_id = fields.Many2one('res.partner', string="Partner",
                                 required=True
                                 )
    property_id = fields.Many2one('estate.property',
                                  required=True
                                  )

    date_deadline = fields.Datetime(
        compute='_compute_date_deadline',  inverse='_inverse_date_deadline')

    validity = fields.Integer(string="Validity (days)", default=7)

    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            now = record.create_date if record.create_date else datetime.now()
            record.date_deadline = now + relativedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            delta = record.date_deadline - record.create_date
            record.validity = delta.days

    def action_accept(self):
        for record in self:
            record.status = 'accepted'
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
            for offer in record.property_id.offer_ids:
                if offer.id != record.id and offer.status == 'accepted':
                    offer.status = None

    def action_refuse(self):
        for record in self:
            record.status = 'refuse'
