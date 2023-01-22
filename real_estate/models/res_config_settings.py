""" from odoo import models,fields

class ConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    group_description = fields.Boolean("Show description", group='base.group_user',
    implied_group='real_estate:group_description')

    module_note = fields.Boolean("Install real estate app") """