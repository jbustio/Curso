

from odoo import models, fields, api


class real_estate(models.Model):
    _name = 'real_estate.real_estate'
    _description = 'real_estate.real_estate'

    name = fields.Char(required=True)
    description = fields.Text()
    property_type_id = fields.Many2one('estate.type',"Type",ondelete="cascade")
    tag_id = fields.Many2many('estate.tag',string="Tags")
    offer = fields.One2many('estate.offer','property_id',string="Offer")
    salesperson = fields.Many2one('res.users',string="Salesperson",index=True, default=lambda self:self.env.user)
    buyer = fields.Many2one('res.partner',string="Buyer")
    postcode = fields.Char()
    date_availability = fields.Date()
    expected_price = fields.Float(required=True)
    selling_price = fields.Float()
    
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden area')
    total_area = fields.Float('Total Area',compute="_compute_area")
    garden_orientation = fields.Selection([
        ('North', 'North'),
        ('South', 'South'),
        ('East', 'East'),
        ('West', 'West'),
    ], string='Garden orientation')
    
    @api.depends("garden_area","living_area")
    def _compute_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area


