

from odoo import models, fields, api

class Type(models.Model):
    _name = 'estate.type'
    _description = 'Propiedad que indica el tipo de propiedad'
    _order = "sequence,name"

    name = fields.Char()
    property_ids = fields.One2many('real_estate.real_estate','property_type_id',string="Houses")
    sequence = fields.Integer()
    offer_ids = fields.One2many('estate.offer','property_type_id',string="Offers")
    offer_count = fields.Integer(compute="_count_offers")

    @api.depends("offer_ids")
    def _count_offers(self):
        for record in self:
            record.offer_count += len(record.offer_ids)
            
            # if record.offer_ids:
            #     print("*************************",self.offer_ids)
                