from odoo import models, fields, api


class tag(models.Model):
    _name = 'estate_property.tag'
    _description = 'Tags for appartment classification'
    _order = 'name'

    name = fields.Char(required=True)
    estate_id = fields.Many2many(
        'estate_property.estate.property',
        string="Houses")
    color = fields.Integer()
