
from odoo import models, fields, api

class Offer(models.Model):
    _name="estate.offer"
    _description="Ofertas hechas"

    price = fields.Float()
    status = fields.Selection([('accepted','Accepted'),('refused','Refused')],string="Status")
    partner_id = fields.Many2one('res.partner',string="Partner",required=True)
    property_id = fields.Many2one('real_estate.real_estate',string="Property")
    