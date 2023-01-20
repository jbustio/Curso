from odoo import fields, models



class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    
    
    name = fields.Char( "Property Name",required=True)
    expected_price = fields.Float(string = "Expected Property Price",required=True)
    description = fields.Text("Description")
    postcode = fields.Char(string = "Postal Code")
    date_availability =fields.Date(string = "Availavility Date")
    selling_price = fields.Float(string  = "Selling Price")
    bedrooms = fields.Integer(string = "Number of Bedrooms")
    living_area = fields.Integer(string = "Number of Living Areas")
    facades = fields.Integer(string = "Number of Facades")
    garage = fields.Boolean(string = "Has a Garage")
    garden = fields.Boolean(string = "Has a Garden")
    garden_area = fields.Integer(string = "Garden Area")
    garden_orientation = fields.Selection([("N","North"), ("S","South"),("E", "East"),("W", "West")])
    
    property_type_id = fields.Many2one('property.type', 'Property Type')
    
    #property_tag_ids = fields.Many2many('property.tag', 'Property Tag')


