from odoo import fields, models


class InheritedUser(models.Model):
    _inherit = 'res.users'

    property_ids = fields.One2many("state_property.state_property", "user_id", domain=[("state", "in", ["new", "offer_received"])])
