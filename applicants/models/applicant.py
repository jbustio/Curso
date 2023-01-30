# -*- coding: utf-8 -*-

from odoo import models, fields, api
from pydantic import ValidationError
import re

class applicants(models.Model):
    _name = 'applicants.applicants'
    _description = 'applicants.applicants'

    name = fields.Char(required = True, string = 'Name')
    last_name1 = fields.Char(string = 'Last Name1')
    last_name2 = fields.Char(string="Last Name2")
    ci = fields.Char(required=True, string="CI")
    address = fields.Char(required=True, string="address")
    age = fields.Integer(required=True, string="Age", default=18)
    sex = fields.Selection([
        ('Female', 'Female'),
        ('Male', 'Male')
    ], string='Sex')
    company_id = fields.Many2many('res.partner', string='Company')
    technology_and_experience_id = fields.One2many(
        'applicants.technology_and_experience',
        'applicant_id',
        string="Technology and experience"
        )

    _sql_constraints = [
        (
            'check_age_lgq_18', 
            'CHECK(age >= 18)',
            'The applicant must be in legal age'
        )
    ]

    @api.constrains('ci')
    def _check_ci(self):
        reg = re.compile("\d{11}")
        for record in self:
            if not reg.fullmatch(record.ci):
                raise ValidationError("The CI must be a number of eleven digits")

