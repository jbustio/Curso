from odoo import api, fields, models
from dateutil.relativedelta import relativedelta
from datetime import datetime

from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Real Estate Property'
    _order = "id desc"

    _sql_constraints = [
        ('expected_price_positive', 'CHECK (expected_price > 0)', 'Price must be positive'),
        ('selling_price_positive', 'CHECK (selling_price > 0)', 'Price must be positive'),
    ]

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

    @api.constrains('selling_price')
    def _check_expected_price(self):
        for record in self:
            ninety_percent = record.expected_price / 100 * 90
            if float_compare(record.selling_price, ninety_percent, 2) == -1:
                raise ValidationError("Selling price cannot be lower than 90%")


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'PropertyType'

    _rec_name = 'name'
    _order = 'name ASC'

    _sql_constraints = [
        ("estate_property_type_name", "UNIQUE (name)",
         "Name must be unique."),
    ]


    name = fields.Char(
        string='Name',
        required=True,
    )

    property_ids = fields.One2many(
        "estate.property", "property_type_id", string="Real Estates")
    sequence = fields.Integer(
        default=1, help="Used to order. Lower is better.")

    offer_ids = fields.One2many('estate.property.offer', 'property_type_id')
    offer_count = fields.Integer(compute="_compute_offer_count",
                                 readonly=True
                                 )

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = record.offer_ids.search_count([])


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'PropertyTag'

    _rec_name = 'name'
    _order = 'name ASC'

    _sql_constraints = [
        ("estate_property_tag_name", "UNIQUE (name)",
         "Name must be unique."),
    ]

    name = fields.Char(
        string='Name',
        required=True,
    )
    color = fields.Integer()


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'EstatePropertyOffer'
    _order = "price desc"

    _sql_constraints = [
        ('expected_price', 'CHECK (price > 0)', 'Price must be positive'),
    ]

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
    property_type_id = fields.Many2one(
        string="Property Type", related='property_id.property_type_id', store=True)

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
            q = record.property_id.offer_ids.search([
                ('status', '=', 'accepted'),
                '!', ('id', '=', record.id),
            ])
            for o in q:
                o.status = None

            record.status = 'accepted'
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
            record.property_id.state = "offer_accepted"

    def action_refuse(self):
        for record in self:
            if record.status == 'accepted':
                record.property_id.state = "offer_receive"
            record.status = 'refuse'
