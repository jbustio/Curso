import datetime
from datetime import timedelta

from odoo import api, models, fields
from dateutil.relativedelta import relativedelta

from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'
    _order = 'id desc'
    
    name = fields.Char('Name', required=True)
    description = fields.Text('Description')
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=fields.datetime.now() + relativedelta(months=3))
    active= fields.Boolean('Active',default=True)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([
        ('north', 'North'),('south','South'),('east','East'),('west','West'),
    ], string='Garden Orientation')
    property_type_id = fields.Many2one('estate.property.type', string='Property Type')
    tag_ids = fields.Many2many('estate.property.tag')
    offer_ids = fields.One2many('estate.property.offer','property_id', string='Offer')
    state = fields.Selection([
        ('new', 'New'), ('o_r','Offer Received'),
        ('o_ac','Offer Acepted'),('s','Sold'),('c','Canceled')], 
         required=True,copy=False, default='new')
    total_area = fields.Float(compute='_compute_area', string='Total Area')
    best_price = fields.Char(compute='_compute_best_price', string='Best Price')
    sales_person = fields.Many2one('res.users',string="Sales person",default=lambda self: self.env.user)
    buyer = fields.Many2one('res.partner',string="Buyer")
    
    _sql_constraints = [
        ('expected_price', 'CHECK(expected_price > 0 )',
         'The expected price must be strictly positive'),
        ('selling_price','CHECK(selling_price >= 0 )' ,'The selling price must be positive')
    ]
    @api.constrains('selling_price')
    def _check_selling_value(self):
       value = self.expected_price * 0.9
       if self.selling_price >0 and float_compare(self.selling_price,value ,1) == -1:
           raise ValidationError("The selling price not lower than 90% the expected price")

    @api.depends('offer_ids')
    def _compute_best_price(self):
        if self.offer_ids != None:
            temp = []
            for off in self.offer_ids:
                temp.append(off.price)
            if len(temp) !=0:
                self.best_price = max(temp)
            else:
                self.best_price =0
        

    @api.depends("living_area","garden_area")
    def _compute_area(self):
        for record in self:
            record.total_area = record.living_area +record.garden_area
            
    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area =10
            self.garden_orientation = 'north'
        else:
            self.garden_area =0
            self.garden_orientation = ''    
    
    def action_cancel(self):
        for record in self:
            if not record.state == "s":
                raise UserError(("A sold property cannot be canceled !"))
            record.state = "c"                
        return True
    
    def action_sold(self):
        for record in self:
            if not record.state == 'c':
                raise UserError(("A canceled property cannot be sold !"))
            record.state = "s"
        return True
class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type'
    _order = 'name asc'

    name = fields.Char('Type', required=True)
    sequence = fields.Integer()
    _sql_constraints = [
        ("name_check", "UNIQUE(name)", "The name is unique"),
    ]

    offer_ids = fields.One2many('estate.property.offer','property_id')
    property_ids = fields.One2many('estate.property', 'property_type_id')
    offer_count = fields.Integer(compute = "_compute_offer_count")
    
    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count += len(record.offer_ids)


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate Property Tag'
    _order = 'name asc'
    
    name = fields.Char(required=True)
    color = fields.Integer('Color')
    _sql_constraints = [
        ("name_check", "UNIQUE(name)", "The name is unique"),
    ]
class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'
    _order = 'price desc'

    price = fields.Float('price')
    status = fields.Selection([
        ('accepted', 'Accepted'),('refused','Refused')
    ], string='status')
    partner_id = fields.Many2one('res.partner', string='partner', required=True)
    property_id = fields.Many2one('estate.property', string='property',required=True)
    validity = fields.Integer('Validity', default=7)
    date_deadline = fields.Char(compute='_compute_date_deadline',inverse='_inverse_date_deadline', string='Date deadline')
    
    _sql_constraints = [
        ('price', 'CHECK(price > 0 )',
         'The offer price must be strictly positive')
    ]
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date != None:
                    record.date_deadline = record.create_date + timedelta(days=record.validity)
    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline != None:
                        # record.create_date = record.date_deadline - timedelta(days=record.validity)
                    record.create_date= datetime.datetime.now()

    def action_accept(self):
        self.status = 'accepted'
        self.property_id.state = 'o_ac'
        self.property_id.selling_price = self.price
        self.property_id.buyer = self.partner_id.id
    
    def action_refuse(self):
        self.status = 'refused'

class ResUsers(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many(
        "estate.property", "sales_person", string="Propertys", domain=[("state", "in", ["new", "o_r"])]
    )