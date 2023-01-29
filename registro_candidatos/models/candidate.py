# -*- coding: utf-8 -*-

import re
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Candidate(models.Model):
    _inherit = 'res.partner'

    _sql_constraints = [
        ('dni_uniq', 'unique(dni)', _('Sorry, exist a candidate with this dni')),
    ]

    values_gender = [('f', 'Femenino'), ('m', 'Masculino')]

    dni = fields.Char("DNI", required=True)
    address = fields.Text("Current address")
    age = fields.Integer("Age")
    gender = fields.Selection(selection=values_gender, string="Gender")
    register_id = fields.One2many("register.candidate", "candidate_id", string="Register of the candidates")

    @api.constrains('dni')
    def validate_dni(self):
        for record in self:
            if len(record.dni) != 11:
                raise ValidationError(_("El carne de identidad debe tener una longitud de 11 digitos"))
            elif re.match(r"^[a-zA-Z][ a-zA-Z]*", record.dni):
                raise ValidationError(_("El carne de identidad no puede contener letras"))

                # /*+~!@#$%^&()_`¡¿?=·ª{}:;'><,.
