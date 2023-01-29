# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class Tecnologia(models.Model):
    _name = 'tech.technology'
    _description = 'Tecnología'

    _sql_constraints = [
        ('name_uniq', 'unique(name)', _('Sorry, exists this technology')),
    ]

    name = fields.Char("Tecnology", required=True)
    registro_id = fields.One2many("register.candidate", "tech_id", string="Registro de candidatos")
