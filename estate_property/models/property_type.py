from odoo import models, fields, api

class proprety_type(models.Model):
    _name = 'estate_property.property.type'
    _description = 'Shows property type'
    _order = 'sequence, name'
    
    offer_ids = fields.One2many(
        'estate_property.offer',
        'property_type_id')
    name = fields.Char(required = True)
    property_ids = fields.One2many(
        'estate_property.estate.property', 
        'property_type_id')
    sequence = fields.Integer(
        'Sequence', 
        help="Used to order stages. Lower is better."
        )
    offer_count = fields.Integer(compute = "_compute_count")

    @api.depends('offer_ids')
    def _compute_count(self):
        for record in self:
            if record.offer_ids.ids:
                record.offer_count = len(record.offer_ids.ids)
            else:
                record.offer_count = 0
