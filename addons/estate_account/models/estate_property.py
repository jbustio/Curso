from odoo import models

class EstateProperty(models.Model):
    _inherit="estate.property"

    def set_property_as_sold(self):
        print('IT IS WORKING!!!')
        return super().set_property_as_sold()
