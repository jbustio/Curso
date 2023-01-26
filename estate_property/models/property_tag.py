from odoo import fields, models



class PropertyTag(models.Model):
    _name = "property.tag"
    _description = "Property Tag"
    _order = "name"
    
    name = fields.Char( "Property Tag")
    
    estate_id = fields.Many2many('estate.property',string="Houses")
    color = fields.Integer('Color')
    
    