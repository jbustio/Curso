

from odoo import models, fields, api

class Type(models.Model):
    _name = 'estate.type'
    _description = 'Propiedad que indica el tipo de propiedad'

    name = fields.Char()
    property_id = fields.One2many('real_estate.real_estate','property_type_id',string="Houses")