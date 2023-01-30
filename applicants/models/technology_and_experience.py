from odoo import models, fields, api
from psycopg2 import IntegrityError

class technology_and_experience(models.Model):
    _name = 'applicants.technology_and_experience'
    _description = 'applicants.technology_and_experience'
    _order = "year desc"

    name = fields.Char(required=True)
    year = fields.Integer(default=1)
    applicant_id = fields.Many2one(
        'applicants.applicants',
        string="Applicant"
    )

    _sql_constraints = [
        (
            'check_years_positive', 
            'CHECK(year >= 1)',
            'Year experience must be positive'
        )
    ]

    @api.constrains('name', 'applicant_id')
    def limit_to_one_tech_by_applicant(self):
    
        if self.env['applicants.technology_and_experience'].search_count([
            '&',
            ('name', '=', self.name),
            ('applicant_id', '=', self.applicant_id.id)
        ]) > 1:
            raise IntegrityError("You can't reinsert technology experience for the same user")
    
