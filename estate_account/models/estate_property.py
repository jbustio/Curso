from odoo import models,fields,api
from odoo import Command


#Extended model with traditional inheritance
class estate_property(models.Model):
    _inherit = "real_estate.real_estate"

    def sold(self):
        print("**************************************")
        print("Is working the overrided method")
        for record in self:
            record_name = record.name
            record_id = record.mapped('offer.partner_id.name')
            
        
     
        #Here I create the invoice
        self.env['account.move'].create({
            'partner_id':record.buyer.id,
            'move_type':'out_invoice',
        
        #Here I create the invoice lines
        
            
            "invoice_line_ids":[
                Command.create({
                    "name":"6'%' of the selling price",
                    "quantity":1,
                    "price_unit":record.selling_price * 0.06,
                }),
                Command.create({
                    "name":"Administrative fee of 100 $",
                    "quantity":1,
                    "price_unit": 100,
                })
            ],
        }) 
        return super().sold()