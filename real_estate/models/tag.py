from odoo import models, fields, api

class Tag(models.Model):
    _name = "estate.tag"
    _description = "Etiquetas para clasificar los apartamentos"
    _order = "name"


    name = fields.Char(required=True)
    estate_id = fields.Many2many('estate.property',string="Houses")
    color = fields.Integer()