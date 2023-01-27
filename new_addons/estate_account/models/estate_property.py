
from odoo import models
from odoo.fields import Command


class EstateProperty(models.Model):
    _name = 'EstateProperty'
    _description = 'Estate Property'
    _inherit = 'estate.property'

    def action_sold_owerride(self):
        print('Hello')        
        self.env['account.move'].create({
            'partner_id': self.buyer.id,
            'move_type': 'out_invoice',
            'invoice_line_ids':[
                Command.create({
                    "name":"6'%' selling price",
                    "quantity":1,
                    "price_unit":self.selling_price * 0.06,
                }),
                Command.create({
                    "name":"100 from administrative fees",
                    "quantity":1,
                    "price_unit": 100,
                })
            ],
        })
        return super().action_sold()

    