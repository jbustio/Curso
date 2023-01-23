# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from datetime import date, timedelta

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
            if record.offer:
                record.best_price = max(record.offer.mapped('price'))

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

class proprety_type(models.Model):
    _name = 'estate_property.property.type'
    _description = 'Shows property type'
    _order = 'sequence, name'
    
    offer_ids = fields.One2many(
        'estate_property.offer',
        'property_type_id')
    name = fields.Char(required = True)
    property_ids = fields.One2many(
        'estate_property.estate.property', 
        'property_type_id')
    sequence = fields.Integer(
        'Sequence', 
        help="Used to order stages. Lower is better."
        )
    offer_count = fields.Integer(compute = "_compute_count")

    @api.depends('offer_ids')
    def _compute_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids.mapped(record.name))

class tag(models.Model):
    _name = 'estate_property.tag'
    _description = 'Tags for appartment classification'
    _order = 'name'

    name = fields.Char(required=True)
    estate_id = fields.Many2many(
        'estate_property.estate.property',
        string="Houses")
    color = fields.Integer()

class offer(models.Model):
    _name="estate_property.offer"
    _description="Offerts done"
    _order = 'price desc'

    price = fields.Float()
    status = fields.Selection([
        ('accepted','Accepted'),
        ('refused','Refused')
        ],
        string="Status")
    partner_id = fields.Many2one(
        'res.partner',
        string="Partner",
        required=True)
    property_id = fields.Many2one(
        'estate_property.estate.property',
        string="Property"
    )
    property_type_id = fields.Many2one(
        related = "property_id.property_type_id"
    )
    create_date = fields.Date(
            readonly = True,
            string = 'Create date',
            default= date.today()
    )
    validity = fields.Integer(
                default = 7,
                string = 'Validity(Days)')
    date_deadline = fields.Date(
        string = "Deadline",
        compute = "_compute_date_deadline",
        inverse = "_inverse_date_deadline"
    )
    property_state = fields.Selection(
        string = "State",
        related = "property_id.state"
        )


    @api.depends('date_deadline', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = date(
                year = record.create_date.year, 
                month = record.create_date.month, 
                day = record.create_date.day
            ) + timedelta(days = record.validity)
        
    def _inverse_date_deadline(self):
        for record in self:
            d = date(
                year = record.date_deadline.year, 
                month = record.date_deadline.month, 
                day = record.date_deadline.day
            ) - timedelta(days = record.validity)
            record.create_date = d
            record.validity = (record.date_deadline - record.create_date).days
        
    def action_accept(self):
        for record in self:
            if record.property_id.state == 'Offer Accepted':
                raise exceptions.UserError("Pay attention: Only one offer can be accepted for a given property")
            record.property_id.state = 'Offer Accepted'
            record.property_id.buyer = record.partner_id
            record.property_id.selling_price = record.price
            record.status = 'accepted'


    def action_refuse(self):
        for record in self:
            record.property_id.state = 'Offer Refused'
            record.status = 'refused'
