from odoo import fields, models, Command




class EstateProperty(models.Model):
    _description = 'Estate Account Model, that inherits from Account and Estate Property Modules'
    _inherit = 'estate.property'

    name = fields.Char()
    description = fields.Text()
    
    
    #Overriding the action sold from : Estate Property
    def action_sold(self):
        super_call = super().action_sold()
        print("executing New Method")
        for r in self:
            #self.env['account.move'].create({'partner_id': r.buyer.id, 'move_type': 'out_invoice', 'invoice_line_ids': 
            #})
            continue
        return super_call