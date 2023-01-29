from odoo import models, fields


class technology_and_experience(models.Model):
    _name = 'applicants.technology_and_experience'
    _description = 'applicants.technology_and_experience'

    name = fields.Char(required=True)
    year = fields.Integer(default=1)
    applicant_id = fields.Many2one(
        'applicants.applicants',
        string="Applicant"
    )