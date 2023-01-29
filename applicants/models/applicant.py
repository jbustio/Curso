# -*- coding: utf-8 -*-

from odoo import models, fields, api
from pydantic import ValidationError
import re

class applicants(models.Model):
    _name = 'applicants.applicants'
    _description = 'applicants.applicants'

    name = fields.Char(required = True, string = 'Name')
    lastName1 = fields.Char(string = 'Last Name1')
    lastName2 = fields.Char(string="Last Name2")
    CI = fields.Char(required=True, string="CI")
    address = fields.Char(required=True, string="address")
    Age = fields.Integer(required=True, string="Age")
    Sex = fields.Selection([
        ('Female', 'Female'),
        ('Male', 'Male')
    ], string='Sex')
    company_id = fields.Many2many('res.partner', default = 'Company')
    technology_and_experience_id = fields.One2many(
        'applicants.technology_and_experience',
        'applicant_id',
        string="Technology and experience"
        )

    

    @api.constrains('CI')
    def _check_CI(self):
        reg = re.compile("\d{11}")
        for record in self:
            if not reg.fullmatch(record.CI):
                raise ValidationError("The CI must be a number of eleven digits")

