from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
from datetime import timedelta
from odoo.tools.float_utils import * 

class real_estate(models.Model):
    _name = 'real_estate.real_estate'
    _description = 'Modelo principal en la app real estate para el manejo de los bienes raices'
    _order = "id desc"

    _sql_constraints = [
         ('check_expected_price','CHECK(expected_price > 1)','The expected price should be strictly positive'),
         ('check_selling_price','CHECK(selling_price >= 1)','The selling price must be positive'),
         ('unique_tag','UNIQUE(tag_id)','The tag must be unique'),
         ('unique_type','UNIQUE(property_type_id)','The type must be unique'),
        ]

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
    expected_price = fields.Float(required=True, default=1)
    selling_price = fields.Float(readonly=True,copy=False)
    best_price = fields.Float(compute="_compute_price",default=0)
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
    state = fields.Selection(selection=[
        ('New','New'),
        ('Offer Received','Offer Received'),
        ('Offer Accepted','Offer Accepted'),
        ('Sold','Sold'),
        ('Canceled','Canceled'),
    ],string="Status",default="New")


    def sold(self):
        if self.state == 'New':
            self.state = 'Sold'
        elif self.state == 'Canceled':
            raise UserError("Canceled properties cannot be set to sold state")
        else:
            self.state = "Sold"
    def cancel(self):
        self.state = 'Canceled'


    def populate(self):
        self.create({
            "name":"Dummy House",
            "description":"The description",
            "property_type_id":self.env['estate.type'].create({"name":"Testing Type"}),
            "tag_id":self.env["estate.tag"].create({"name":"Testing Tag"})
        })


    @api.depends("garden_area","living_area")
    def _compute_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area


   



    #This method compute the best price
    @api.depends("offer.price")
    def _compute_price(self):
        prices_to_iter = []
        for record in self:
            if len(record.offer) > 0:
                #for offer in record.offer:
                try:
                    record.best_price = max(record.mapped('offer.price'))
                except ValueError:
                    return UserError("Error en el best price")
            else:
                record.best_price = 0
    
   

    @api.onchange('garden')
    def _onchange_garden(self):
        for record in self:
            if (record.garden == True):
                record.garden_area = 10
                record.garden_orientation = 'North'
            else:
                record.garden_area = 0
                record.garden_orientation = ''


    #############################
    """Python constraints"""
    @api.constrains('selling_price')
    def _check_selling_price(self):
        for record in self:
            if (record.selling_price < record.expected_price * 0.9)and not(float_is_zero(record.selling_price,10)):
                raise ValidationError("El precio de venta no puede ser menor del 90'%' del esperado")
    #############################
    """ Method for testing  """
    def north_direction(self):
        self.write({'garden_orientation':'North'})

    def south_direction(self):
        self.write({'garden_orientation':'South'})

    ##############################