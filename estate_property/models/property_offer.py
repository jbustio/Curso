from odoo import fields, models



class PropertyOffer(models.Model):
    _name = "property.offer"
    _description = "Property Offer"
    
    price = fields.Float( "Price")
    status = fields.Selection([("A","Accepted"), ("R","Refused")], copy = False)
    partner_id = fields.Many2one('res.partner',string="Partner", required=True)
    property_id = fields.Many2one('estate.property',string="Property", required=True)