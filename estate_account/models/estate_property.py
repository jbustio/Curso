import datetime

from odoo import models, Command
from odoo import models, fields, api


class RealEstatePropertyAccountModel(models.Model):
    _inherit = "real.estate.property"

    invoice_id = fields.Many2one('account.move', string="Invoice")

    def _calc_selling_price_percent(self, selling_price):
        return selling_price * 0.06

    def sell_property(self):
        invoice_vals = {

            'name': f'realestate/{self.property_type_id.name}/{self.id}',
            'move_type': 'out_invoice',
            'partner_id': self.buyer_id.id,
            'invoice_date': datetime.datetime.today(),
            "line_ids": [
                (0, 0, {
                    "name": f"{self.name} (6%)",
                    "quantity": "1",
                    "price_unit": self._calc_selling_price_percent(self.selling_price),
                    "tax_ids": False
                }),
                (0, 0, {
                    "name": "administrative fees",
                    "quantity": "1",
                    "price_unit": 100.00,
                    "tax_ids": False

                })
            ],

        }
        self.invoice_id = self.env['account.move'].create(invoice_vals)
        return super().sell_property()