# -*- coding: utf-8 -*-

from odoo import models, fields
from odoo import Command


class estate_account(models.Model):
    _description = 'estate_account.estate_account'
    _inherit = 'estate_property.estate.property'

    name = fields.Char()
    description = fields.Text()

    def action_sold(self):
        res = super().action_sold()
        for record in self:
            self.env['account.move'].create({
                'partner_id': record.buyer.id,
                'move_type': 'out_invoice',
                'invoice_line_ids': [
                    Command.create({
                        "name": "6'%' of sold price",
                        "quantity": 1,
                        "price_unit": (record.selling_price / 100) * 6,
                    }),
                    Command.create({
                        "name": "Administrative fees",
                        "quantity": 1,
                        "price_unit": 100,
                    })
                ]
            })
        return res


    