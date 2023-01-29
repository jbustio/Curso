from odoo import models, Command

class EstateProperty(models.Model):
    _inherit="estate.property"

    def set_property_as_sold(self):
        print('INSIDE')
        move = self.env['account.move'].create({'partner_id':self.buyer_id, 'move_type':'out_invoice',
                                                    'invoice_line_ids':[Command.create({'name':'Tax', 
                                                    'quantity':self.selling_price * 6 /100, 'price_unit':self.selling_price})
                                                    ,Command.create({'name':'Administrative Fees', 'quantity':100, 'price_unit':0})]})
        return super().set_property_as_sold()
