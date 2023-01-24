from odoo import fields, models



class PropertyType(models.Model):
    _name = "property.type"
    _description = "Property Type"
    
    
    name = fields.Char( "Property Type",required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id')
    sequence = fields.Integer('Sequence')
    