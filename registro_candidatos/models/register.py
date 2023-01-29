# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class RegisterCandidate(models.Model):
    _name = 'register.candidate'
    _description = 'Register candidate'

    _sql_constraints = [
        ('candidate_tech_uniq', 'unique(candidate_id, tech_id)', _('Sorry, exists a relation between candidate-tecnology')),
        ('check_experience', 'check (experience > 0)', 'Los años de experiencia deben ser mayor a cero.')
    ]
    candidate_id = fields.Many2one("res.partner", string="Candidate", required=True)
    tech_id = fields.Many2one("tech.technology", string="Technology", required=True)
    experience = fields.Integer("Experience (Years)", required=True)
