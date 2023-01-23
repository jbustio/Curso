from odoo import fields, models, api
from datetime import date


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    
    
    name = fields.Char( "Property Name",required=True)
    expected_price = fields.Float(string = "Expected Property Price",required=True)
    description = fields.Text("Description")
    postcode = fields.Char(string = "Postal Code")
    date_availability =fields.Date(string = "Availavility Date", copy = False, default = date(year = date.today().year, month= date.today().month + 3, day = date.today().day) )
    selling_price = fields.Float(string  = "Selling Price" , readonly=True, copy = False)
    bedrooms = fields.Integer(string = "Number of Bedrooms", default = 2)
    living_area = fields.Integer(string = "Number of Living Areas")
    facades = fields.Integer(string = "Number of Facades")
    garage = fields.Boolean(string = "Has a Garage")
    garden = fields.Boolean(string = "Has a Garden")
    garden_area = fields.Integer(string = "Garden Area")
    garden_orientation = fields.Selection([("N","North"), ("S","South"),("E", "East"),("W", "West")])
    active = fields.Boolean(string = "Active", default = True)
    state = fields.Selection([('New', 'New'),('Offer Received', 'Offer Received'),('Offer Refused', 'Offer Refused'), ('Offer Accepted', 'Offer Accepted'), ('Sold', 'Sold'),('Canceled', 'Canceled')], required=True, copy = False, default = 'New')
    
    
    
    
    property_type_id = fields.Many2one('property.type', 'Property Type')
    property_tag_ids = fields.Many2many('property.tag','name', 'Property Tag')
    offer = fields.One2many('property.offer', 'property_id', string="Offers")
    buyer = fields.Many2one('res.partner', string='Buyer', copy = False)
    sales_person = fields.Many2one('res.users', string='Salesperson',  default=lambda self: self.env.user)
    total_area = fields.Integer(compute = "_compute_total_area")

    @api.depends('living_area','garden_area')
    def _compute_total_area(self):
            for f in self:
                f.total_area = f.living_area + f.garden_area
