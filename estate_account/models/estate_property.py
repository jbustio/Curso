from odoo import models, Command


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sell(self):
        """
    Add the second step of invoice creation.
    Create an empty account.move in the override of the action_sold method:
        the partner_id is taken from the current estate.property
        the move_type should correspond to a ‘Customer Invoice’
    Tips:
        to create an object, use self.env[model_name].create(values), where values is a dict.
        the create method doesn’t accept recordsets as field values."""

        """


        6% of the selling price
        an additional 100.00 from administrative fees

        """
        # out_invoice
        print("()()))action inherited working")
        for record in self:
            self.env['account.move'].create({
                "partner_id": record.buyer_id.id,
                "move_type": 'out_invoice',
                "invoice_line_ids": [
                    # name, quantity and price_unit
                    # Command.create({
                    #     "name": record.name,
                    #     "quantity": 1,
                    #     "price_unit": record.selling_price,
                    # }),
                    Command.create({
                        "name": "6% of sold price",
                        "quantity": 1,
                        "price_unit": record.selling_price / 100 * 6,
                    }),
                    Command.create({
                        "name": "Administrative fees",
                        "quantity": 1,
                        "price_unit": 100,
                    })
                ],
            })
        return super().action_sell()
n