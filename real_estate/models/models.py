# -*- coding: utf-8 -*-
import pytz
from odoo import models, fields, api
import datetime
from dateutil.relativedelta import relativedelta

from odoo.exceptions import ValidationError, UserError


class RealEstatePropertyTag(models.Model):
    _name = 'real.estate.property.tag'
    _description = 'Real Estate Property Tag model class'
    _sql_constraints = [
        ('name_uniq', 'UNIQUE (name)', 'You can\'t have two property types with the same name !')
    ]
    _rec_name = 'name'
    _order = 'name'

    name = fields.Char(
        required=True,
    )
    color = fields.Integer(default=1)


class RealEstatePropertyType(models.Model):
    _name = 'real.estate.property.type'
    _description = 'Real Estate Property Type model class'

    _rec_name = 'name'
    _order = 'sequence,name'
    _sql_constraints = [
        ('name_uniq', 'UNIQUE (name)', 'You can\'t have two property types with the same name !')
    ]
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")

    name = fields.Char(
        required=True
    )
    real_estate_property_ids = fields.One2many('real.estate.property', inverse_name="property_type_id", string="Real Estate Properties")
    offer_ids = fields.One2many('real.estate.property.offer', inverse_name="property_type_id", string="Real Estate Offers")
    offer_count = fields.Integer(compute='_count_offers')

    @api.depends("offer_ids")
    def _count_offers(self):
        for record in self:
            record.offer_count = record.offer_ids.search_count([])


class RealEstateProperty(models.Model):
    _name = 'real.estate.property'
    _description = 'Real Estate Property model class'
    _sql_constraints = [
        ('bedrooms_positive_integer', 'CHECK(bedrooms >= 0)', "The bedrooms must be a positive numeric value"),
        ('living_area_positive_integer', 'CHECK(living_area >= 0)', "The living_area must be a positive numeric value"),
        ('expected_price_positive_integer', 'CHECK(expected_price >= 0)',
         "The expected price must be a positive numeric value"),
        ('selling_price_positive_integer', 'CHECK(selling_price >= 0)',
         "The selling price must be a positive numeric value"),
    ]
    _order = "id desc"
    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=lambda self: datetime.datetime.today() + relativedelta(month=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(copy=False, readonly=True)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer("Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer("Garden Area (sqm)")
    garden_orientation = fields.Selection([('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])
    active = fields.Boolean(default=True)
    state = fields.Selection(required=True, copy=False, default='new',
        selection=[('new', "New"), ('offer_received', "Offer Received"), ('offer_accepted', "Offer Accepted"),
                   ('sold', "Sold"), ('canceled', "Canceled")])

    property_type_id = fields.Many2one('real.estate.property.type', string="Property Type")
    tag_ids = fields.Many2many('real.estate.property.tag', string="Property Tags")
    offer_ids = fields.One2many('real.estate.property.offer', string="Property Offers", inverse_name='property_id')
    buyer_id = fields.Many2one('res.partner', string="Buyer")
    salesman_id = fields.Many2one('res.users', string="Salesman", default=lambda self: self.env.user)

    total_area = fields.Integer("Total Area (sqm)", compute="_compute_total_area")
    best_offer = fields.Float(compute="_compute_best_offer")

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = None

    @api.constrains('garden', 'garden_area')
    def _check_garden_area(self):
        for record in self:
            # check that garden is True
            if record.garden and record.garden_area <= 0:
                raise ValidationError("The garden area must be greater than zero.")

    @api.constrains('garden', 'garden_orientation')
    def _check_garden_orientation(self):
        for record in self:
            # check that garden is True
            if record.garden and not record.garden_orientation:
                raise ValidationError("Please provide an orientation for the garden.")

    @api.depends("garden_area", "living_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + (record.garden_area or 0)

    @api.depends("offer_ids")
    def _compute_best_offer(self):
        for record in self:
            if record.offer_ids:
                if len(record.offer_ids) > 1:
                    record.best_offer = max(record.offer_ids.mapped('price'))
                else:
                    record.best_offer = record.offer_ids[0].price
            else:
                record.best_offer = None

    def sell_property(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("This property has already been sold")

            if record.state != 'canceled':
                record.state = 'sold'
            else:
                raise UserError("Unable to cancel already canceled properties")
        return True

    def cancel_property(self):
        for record in self:
            if record.state == 'canceled':
                raise UserError("This property has already been canceled")

            if record.state != 'sold':
                record.state = 'canceled'
            else:
                raise UserError("Unable to cancel already sold properties")
        return True


class RealEstatePropertyOffer(models.Model):
    _name = 'real.estate.property.offer'
    _description = 'Real Estate Property Offer model class'
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(selection=[("accepted", "Accepted"), ('refused', "Refused")], copy=False)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")
    partner_id = fields.Many2one('res.partner', string="Real Estate Partner")
    property_id = fields.Many2one('real.estate.property', string="Real Estate Property")
    property_type_id = fields.Many2one('real.estate.property.type', string="Property Type",
                                       related="property_id.property_type_id", store=True)

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:

            if record.create_date:
                created_ts = record.create_date
            else:
                created_ts = datetime.datetime.now()
            record.date_deadline = created_ts + datetime.timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date:
                created_ts = record.create_date
            else:
                created_ts = datetime.datetime.now()

            d = record.date_deadline
            delta = d - created_ts.date()
            record.validity = delta.days

    def accept_offer(self):
        # # check if any other offer has been accepted
        # if record.search([("property_id.offer_ids.status", "=", "accepted")]).exists():
        #     raise UserError("This property has already been accepted")
        for record in self:
            data = record.property_id.offer_ids.mapped('status')
            if 'accepted' in data:
                raise UserError("This property has already been accepted")

            if record.status != 'refused':
                record.status = 'accepted'
                record.property_id.buyer_id = record.partner_id
                record.property_id.selling_price = record.price
                record.property_id.state = 'offer_accepted'

                # refuse all other offers
                other_offers = record.property_id.offer_ids.filtered(lambda offer: offer.id != record.id)
                for o in other_offers:
                    o.status = 'refused'
            else:
                raise UserError("Unable to accept an already refused offer")
        return True

    def refuse_offer(self):
        for record in self:
            if record.status == 'refused':
                raise UserError("This property has already been refused")

            if record.status != 'accepted':
                record.status = 'refused'
            else:
                raise UserError("Unable to refuse an already accepted offer")
        return True