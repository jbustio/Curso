from odoo import fields, models


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Real Estate Property'
    _order = 'name ASC'

    name = fields.Char(required=True)
    tags = fields.Many2many('estate.property.tag')
    description = fields.Text()
    postcode = fields.Text()
    date_availability = fields.Date()
    expected_price = fields.Float(required=True)
    selling_price = fields.Float()
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    property_type_id = fields.Many2one("estate.property.type", string="Poperty Type")
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[('north', 'North'), ('south', 'South'),
                   ('east', 'East'), ('west', 'West'),],
    )



class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'PropertyType'

    _rec_name = 'name'
    _order = 'name ASC'

    name = fields.Char(
        string='Name',
        required=True,
    )
    real_estate = fields.One2many("estate.property", "property_type_id", string="Real Estates")




class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'PropertyTag'

    _rec_name = 'name'
    _order = 'name ASC'

    name = fields.Char(
        string='Name',
        required=True,
    )


    
 
