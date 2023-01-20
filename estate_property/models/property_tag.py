from odoo import fields, models



class PropertyTag(models.Model):
    _name = "property.tag"
    _description = "Property Tag"
    
    
    name = fields.Char( "Property Tag",required=True)
    