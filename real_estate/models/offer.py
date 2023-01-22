
from odoo import models, fields, api
from datetime import timedelta

class Offer(models.Model):
    _name="estate.offer"
    _description="Ofertas hechas"

    price = fields.Float(required=True)
    status = fields.Selection([('accepted','Accepted'),('refused','Refused')],string="Status")
    validity = fields.Integer(default=7,string="Validity(days)")
    date_deadline = fields.Date(readonly=True,compute="_compute_date_deadline",inverse="_inverse_date_deadline")
    partner_id = fields.Many2one('res.partner',string="Partner",required=True)
    property_id = fields.Many2one('real_estate.real_estate',string="Property")
    

    @api.depends("validity","create_date")
    def _compute_date_deadline(self):
        for record in self:
            try:
                if record.create_date != None:
                    record.date_deadline = fields.Date(self.create_date).add(fields.Date.to_date(fields.Date.today()+ timedelta(days=self.validity)))
            except ValueError as e:
                print(e)
    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline:
                record.create_date = fields.Date(self.date_deadline).subtract(fields.Date.to_date(fields.Date.today()+timedelta(days=self.validity)))