from odoo import models, fields, api
from datetime import date, timedelta

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

    _sql_constraints = [
        (
            'check_offer_price', 
            'CHECK(price >= 0)',
            'An offer price must be strictly positive'
        )
    ]

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
