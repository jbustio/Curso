# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from odoo.tools.float_utils import * 
from datetime import date

from pydantic import ValidationError

class estate_property(models.Model):
    _name = 'estate_property.estate.property'
    _description = 'estate_property.estate_property'
    _order = "id desc"

    name = fields.Char(required = True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
                        copy = False, 
                        default = date(year = date.today().year, 
                                        month= date.today().month + 3, 
                                        day = date.today().day),
                        string = "Date availability")
    expected_price = fields.Float(
                    required = True, 
                    string = 'Expected price'
                )
    selling_price = fields.Float(
                    readonly = True,
                    copy = False,
                    string = 'Selling price')
    bedrooms = fields.Integer(default = 2, string = 'Bedrooms')
    living_area = fields.Integer(string = 'Living area')
    facades = fields.Integer(string = 'Facades')
    garage = fields.Boolean(string = 'Garage')
    garden = fields.Boolean(string = 'Garden')
    garden_area = fields.Integer(string = 'Garden area')
    garden_orientation = fields.Selection([
        ('North', 'North'),
        ('South', 'South'),
        ('East', 'East'),
        ('West', 'West'),
    ], string='Garden orientation')
    active = fields.Boolean(default = True)
    state = fields.Selection([
        ('New', 'New'),
        ('Offer Received', 'Offer Received'),
        ('Offer Refused', 'Offer Refused'), 
        ('Offer Accepted', 'Offer Accepted'), 
        ('Sold', 'Sold'),
        ('Canceled', 'Canceled')
    ])
    property_type_id = fields.Many2one(
                            "estate_property.property.type", 
                            string = "Type",
                            ondelete = "cascade")
    offer = fields.One2many(
                            'estate_property.offer',
                            'property_id',
                            string="Offer")
    salesperson = fields.Many2one(
                                'res.users',
                                string="Salesperson",
                                index=True, 
                                default=lambda self:self.env.user)
    buyer = fields.Many2one('res.partner',string="Buyer")
    tag_id = fields.Many2many('estate_property.tag',string="Tags")
    total_area = fields.Integer(compute = "_compute_area")
    best_price = fields.Float(compute = "_compute_best_offer_price", default = 0)

    @api.depends('offer')
    def _compute_best_offer_price(self):
        for record in self:
            if record.offer.ids:
                record.best_price = max(record.offer.mapped('price'))
            else:
                record.best_price = 0

    @api.depends('living_area', 'garden_area')
    def _compute_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('value')
    def _value_pc(self):
        for record in self:
            record.value2 = float(record.value) / 100

    """ @api.onchange('garden')
    def _onchange_garden(self):
        for record in self:
            if record.garden:
                record.garden_area = 10
                record.garden_orientation = 'North' """

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'North'

    def action_cancel(self):
        for record in self:
            if record.state == 'Sold':
                raise exceptions.UserError("A sold property cannot be canceled")
            record.state = 'Canceled'

    def action_sold(self):
        for record in self:
            if record.state == 'Canceled':
                raise exceptions.UserError("A canceled property cannot be sold")
            record.state = 'Sold'
    
    _sql_constraints = [
        (
            'check_expected_price', 
            'CHECK(expected_price > 0)',
            'A property expected price must be strictly positive'
        ),
        (
            'check_selling_price', 
            'CHECK(selling_price >= 0)',
            'A property selling price must be positive'
        ),
        (
            'unique_tag',
            'UNIQUE(tag_id)',
            'The tag must be unique'
        ),
        (
            'unique_type',
            'UNIQUE(property_type_id)',
            'The type must be unique'
        )
        
    ]

    @api.constrains('selling_price')
    def _check_selling_price(self):
        for record in self:
            if (record.selling_price < record.expected_price * 0.9) and not(float_is_zero(record.selling_price,10)):
                raise ValidationError("The selling price cannot be lower than 90% of the expected price.")

