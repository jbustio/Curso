from odoo import fields, models, api,exceptions
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
    garden_orientation = fields.Selection([("North","North"), ("South","South"),("East", "East"),("West", "West")])
    active = fields.Boolean(string = "Active", default = True)
    state = fields.Selection([('New', 'New'),('Offer Received', 'Offer Received'),('Offer Refused', 'Offer Refused'), ('Offer Accepted', 'Offer Accepted'), ('Sold', 'Sold'),('Canceled', 'Canceled')], required=True, copy = False, default = 'New')
    best_price = fields.Float(compute = "_compute_price", default = 0)
    
    
    
    property_type_id = fields.Many2one('property.type', 'Property Type')
    property_tag_ids = fields.Many2many('property.tag', string = 'Property Tag')
    #property_tag_ids = fields.Integer()
    offer = fields.One2many('property.offer', 'property_id', string="Offers")
    buyer = fields.Many2one('res.partner', string='Buyer', copy = False)
    sales_person = fields.Many2one('res.users', string='Salesperson',  default=lambda self: self.env.user)
    total_area = fields.Integer(compute = "_compute_total_area")

    @api.depends('living_area','garden_area')
    def _compute_total_area(self):
            for r in self:
                r.total_area = r.living_area + r.garden_area
                
    @api.depends('offer')
    def _compute_price(self):
        for r in self:
            if r.offer:
                r.best_price = max(r.offer.mapped('price'))
                
    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'North'
        else:
            self.garden_area = 10
            self.garden_orientation = ''
            
    
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