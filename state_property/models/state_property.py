# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from odoo.tools.float_utils import float_compare, float_is_zero
from datetime import date
from dateutil.relativedelta import relativedelta


class StateProperty(models.Model):
    _name = 'state_property.state_property'
    _description = 'State property'
    _order = 'id desc'

    _sql_constraints = [
        ('unique_postcode', 'UNIQUE (postcode)', 'Postcode must be unique.'),
        ('check_expected_price', 'CHECK (expected_price < 0)', 'A property expected price must be strictly positive.'),
        ('check_selling_price', 'CHECK (selling_price < 0)', 'A property selling price must be strictly positive.'),
        ('check_bedrooms', 'CHECK (bedrooms < 0)', 'A bedrooms must be strictly positive.')
    ]

    values_orientation = [('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')]
    values_state = [('new', 'New'), ('offer_received', 'Offer received'), ('offer_accepted', 'Offer accepted'),
                    ('sold', 'Sold'), ('canceled', 'Canceled')]

    name = fields.Char("Name", required=True)
    description = fields.Text("Description")
    postcode = fields.Char("Postcode")
    date_availability = fields.Date("Date availability", copy=False, default=lambda x: date.today() + relativedelta(months=3))
    expected_price = fields.Float("Expected price", required=True)
    selling_price = fields.Float("Selling price", readonly=True, copy=False)
    bedrooms = fields.Integer("Bedrooms", default=2)
    living_area = fields.Integer("Living area")
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Garage", default=False)
    garden = fields.Boolean("Garden", default=False)
    garden_area = fields.Integer("Garden area")
    garden_orientation = fields.Selection(selection=values_orientation, string="Garden orientation")
    property_type_id = fields.Many2one("state.property.type", string="State property type", required=True)
    tag_ids = fields.Many2many("state.property.tag", string='Tags')
    active = fields.Boolean("Active", default=True)
    state = fields.Selection(selection=values_state, string="State", required=True, copy=False, default=values_state[0][0])
    total_area = fields.Integer("Total Area", compute="_compute_total_area")
    state_property_offer_id = fields.One2many("state.property.offer", "property_id", string="State property offer")
    buyer = fields.Many2one('res.partner', string='Buyer')
    salesperson = fields.Many2one('res.users', string='Salesperson', index=True, tracking=True, default=lambda self: self.env.user)

    # Method _computed
    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.constrains('date_availability')
    def _check_date_availability(self):
        for record in self:
            if record.date_availability and record.date_availability < fields.Date.today():
                raise ValidationError(_("The entered date availability is not acceptable !"))

    # Method _onchange
    @api.onchange('garden')
    def _onchange_garden(self):
        for record in self:
            if record.garden is True:
                record.garden_area = 10
                record.garden_orientation = 'north'
            else:
                record.total_area = record.total_area - 10
                record.garden_orientation = None
                record.garden_area = 0

    # Actions Buttons
    def action_sold(self):
        for record in self:
            if record.state == 'canceled':
                raise UserError(_("A canceled property cannot be set as sold !"))
            record.state = 'sold'
        return True

    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError(_("A sold property cannot be set as canceled !"))
            record.state = 'canceled'
        return True


class StatePropertyType(models.Model):
    _name = 'state.property.type'
    _description = 'State property type'
    _order = 'name'

    _sql_constraints = [
        ('unique_name', 'UNIQUE (name)', 'A property type name must be unique.')
    ]

    name = fields.Char("Name", required=True)


class StatePropertyTag(models.Model):
    _name = 'state.property.tag'
    _description = 'State property type'
    _order = 'name'

    _sql_constraints = [
        ('unique_name', 'unique (name)', 'A property tag name must be unique.')
    ]

    name = fields.Char("Name", required=True)
