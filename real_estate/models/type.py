

from odoo import models, fields, api

class Type(models.Model):
    _name = 'estate.type'
    _description = 'Propiedad que indica el tipo de propiedad'
    _order = "sequence,name"

    name = fields.Char()
    property_ids = fields.One2many('real_estate.real_estate','property_type_id',string="Houses")
    sequence = fields.Integer()