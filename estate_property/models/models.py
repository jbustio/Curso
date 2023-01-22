# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date

class estate_property(models.Model):
    _name = 'estate_property.estate.property'
    _description = 'estate_property.estate_property'

    name = fields.Char(required = True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy = False, 
                        default = date(year = date.today().year, 
                                        month= date.today().month + 3, 
                                        day = date.today().day))
    expected_price = fields.Float(required = True)
    selling_price = fields.Float(readonly = True, copy = False)
    bedrooms = fields.Integer(default = 2)
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
    active = fields.Boolean(default = True)
    state = fields.Selection([
        ('New', 'New'),
        ('Offer Received', 'Offer Received'), 
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

    @api.depends('living_area', 'garden_area')
    def _compute_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('value')
    def _value_pc(self):
        for record in self:
            record.value2 = float(record.value) / 100



class proprety_type(models.Model):
    _name = 'estate_property.property.type'
    _description = 'Shows property type'

    name = fields.Char(required = True)



class tag(models.Model):
    _name = 'estate_property.tag'
    _description = 'Tags for appartment classification'

    name = fields.Char(required=True)
    estate_id = fields.Many2many(
        'estate_property.estate.property',
        string="Houses")

class offer(models.Model):
    _name="estate_property.offer"
    _description="Offerts done"

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
