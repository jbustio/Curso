

from odoo import models, fields, api
from datetime import timedelta

class real_estate(models.Model):
    _name = 'real_estate.real_estate'
    _description = 'Modelo principal en la app real estate para el manejo de los bienes raices'

    name = fields.Char(required=True,default="New House")
    #groups='real_estate.group_description'
    description = fields.Text('Description',)
    property_type_id = fields.Many2one('estate.type',"Type",ondelete="cascade")
    tag_id = fields.Many2many('estate.tag',string="Tags")
    offer = fields.One2many('estate.offer','property_id',string="Offer")
    salesperson = fields.Many2one('res.users',string="Salesperson",index=True, default=lambda self:self.env.user)
    buyer = fields.Many2one('res.partner',string="Buyer")
    postcode = fields.Char()
    date_availability = fields.Date(copy=False,default=fields.Date.today()+timedelta(days=90),string="Available From")
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True,copy=False)
    best_price = fields.Float(compute="_compute_price")
    bedrooms = fields.Integer(default=2)
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
    active = fields.Boolean('Active',default=True)
    state = fields.Selection([
        ('New','New'),
        ('Offer Received','Offer Received'),
        ('Offer Accepted','Offer Accepted'),
        ('Sold','Sold'),
        ('Canceled','Canceled'),
    ])







    @api.depends("garden_area","living_area")
    def _compute_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends("offer")
    def _compute_price(self):
        prices_to_iter = []
        for record in self:
            if(record.offer != None or record.offer.property_id == record.id):
                for offer in record.offer:
                    prices_to_iter.append(offer.price)
                self.best_price = max(prices_to_iter)
            else:
                self.best_price = 0
    
    #############################
    #Metodos para hacer testing
    def north_direction(self):
        self.write({'garden_direction':'North'})

    def south_direction(self):
        self.write({'garden_direction':'South'})

    ##############################