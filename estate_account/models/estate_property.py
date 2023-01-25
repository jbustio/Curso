from odoo import models, Command


class RealEstatePropertyAccountModel(models.Model):
    _inherit = "real.estate.property"

    def _calc_selling_price_percent(self, selling_price):
        return selling_price * 0.06

    def sell_property(self):
        invoice_vals = {

            'move_type': 'out_invoice',
            'partner_id': self.buyer_id.id,
            "line_ids": [
                Command.create({
                    "name": f"{self.name} (6%)",
                    "quantity": "1",
                    "price_unit": self._calc_selling_price_percent(self.selling_price),
                    "tax_ids": False
                }),
                Command.create({
                    "name": "administrative fees",
                    "quantity": "1",
                    "price_unit": 100.00,
                    "tax_ids": False

                })
            ],

        }
        self.env['account.move'].create(invoice_vals)
        return super().sell_property()