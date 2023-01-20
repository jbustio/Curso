# -*- coding: utf-8 -*-

from odoo import models, fields, api
import datetime
from dateutil.relativedelta import relativedelta

from odoo.exceptions import ValidationError


class RealEstatePropertyTag(models.Model):
    _name = 'real.estate.property.tag'
    _description = 'Real Estate Property Tag model class'

    _rec_name = 'name'
    _order = 'name ASC'

    name = fields.Char(
        required=True,
    )


class RealEstatePropertyType(models.Model):
    _name = 'real.estate.property.type'
    _description = 'Real Estate Property Type model class'

    _rec_name = 'name'
    _order = 'name ASC'
    _sql_constraints = [
        ('name_uniq', 'UNIQUE (name)', 'You can\'t have two property types with the same name !')
    ]

    name = fields.Char(
        required=True
    )
    # real_state_property_ids = fields.One2many('real.estate.property', String="Real Estate Properties")


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

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=lambda self: datetime.datetime.today() + relativedelta(month=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])
    active = fields.Boolean(default=True)

    property_type_id = fields.Many2one('real.estate.property.type', string="Property Type")
    tag_ids = fields.Many2many('real.estate.property.tag', string="Property Tags")
    offer_ids = fields.One2many('real.estate.property.offer', string="Property Offers", inverse_name='property_id')
    buyer_id = fields.Many2one('res.partner', string="Buyer")
    salesman_id = fields.Many2one('res.users', string="Salesman", default=lambda self: self.env.user)

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


class RealEstatePropertyOffer(models.Model):
    _name = 'real.estate.property.offer'
    _description = 'Real Estate Property Offer model class'

    price = fields.Float()
    status = fields.Selection(selection=[("accepted", "Accepted"), ('refused', "Refused")], copy=False)
    partner_id = fields.Many2one('res.partner', string="Real Estate Partner")
    property_id = fields.Many2one('real.estate.property', string="Real Estate Property")
