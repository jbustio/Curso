from odoo import models

class EstateProperty(models.Model):
    _inherit="estate.property"

    def set_property_as_sold(self):
        print('INSIDE')
        move = self.env['account.move'].create({'partner_id':self.buyer_id, 'move_type':'out_invoice'})
        return super().set_property_as_sold()
