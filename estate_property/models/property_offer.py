from odoo import fields, models, api,exceptions

from datetime import date, timedelta


class PropertyOffer(models.Model):
    _name = "property.offer"
    _description = "Property Offer"
    
    price = fields.Float( "Price")
    status = fields.Selection([("Accepted","Accepted"), ("Refused","Refused")], copy = False)
    partner_id = fields.Many2one('res.partner',string="Partner", required=True)
    property_id = fields.Many2one('estate.property',string="Property", required=True)
    created_date = fields.Date(readonly = True,string = 'Created Date',default= date.today())
    validity = fields.Integer( string = "Validity", default = 7)
    date_deadline =fields.Date(string = "Deadline",inverse = "_inverse_date_deadline" ,compute = "_compute_date_deadline")
    
    
    
    @api.depends('date_deadline', 'validity')
    def _compute_date_deadline(self):
        for r in self:
            r.date_deadline = date(year = r.created_date.year, month = r.created_date.month, day = r.created_date.day) + timedelta(days = r.validity)
            
    def _inverse_date_deadline(self):
        for f in self:
            temp = date(year = f.date_deadline.year, month = f.date_deadline.month, day = f.date_deadline.day) - timedelta(days = f.validity)
            f.created_date = temp
            f.validity = (f.date_deadline - f.created_date).days
    
    def action_refuse_offer(self):
        for r in self:
            r.property_id.state = 'Offer Refused'
            r.status = 'Refused'
            
    def action_accept_offer(self):
        for r in self:
            if r.property_id.state == 'Offer Accepted':
                raise exceptions.UserError("You are only able to accept one offer")
            r.property_id.state = 'Offer Accepted'
            r.property_id.buyer = r.partner_id
            r.property_id.selling_price = r.price
            r.status = 'Accepted'


