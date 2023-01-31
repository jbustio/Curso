from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError

class CompanyCandidate(models.Model):
    _name = 'company.candidate'
    _description = 'Candidato de una convocatoria'

    name = fields.Char('Nombre')
    surnames = fields.Char('Apellidos')
    ci = fields.Char('Carnet ID', size=11)
    address = fields.Char('Direccion')
    age = fields.Integer('Edad')
    sex = fields.Selection([
        ('M', 'Masculino') ,
        ('F', 'Femenino')
    ], string='Sexo')
    partner_id = fields.Many2one('res.partner', string='partner')
    technology_ids = fields.One2many('company.technology','candidate_ids' , string='Tecnologias')
    #candidate_technology_ids = fields.One2many('candidatetechnology','candidate_id' ,string='relacion')
    
    _sql_constraints = [
        ("age_check", 'CHECK (age > 18)', 'Debe ser mayor de edad'),
        ('ci_check', 'UNIQUE(ci)','El Carnet ID es unico')
    ]

    @api.constrains('ci')
    def _check_ci(self):
        for record in self:
            if len(record.ci) <11:
                raise ValidationError('El Carnet ID debe tener 11 caracteres')
    
class CompanyTechnology(models.Model):
    _name = 'company.technology'
    _description = 'Tecnologia'
    _order = 'years_experience desc , name'
    name = fields.Selection([
        ('Angular', 'Angular'),
        ('Vue', 'Vue'),
        ('React native', 'React native'),
        ('CSS', 'CSS'),
        ('SprintBoot', 'SprintBoot'),
        ('Odoo', 'Odoo'),
        ('React', 'React'),
        ('Flutter', 'Flutter'),
        ('Python', 'Python'),
        ('HTML', 'HTML'),
        ('AWS', 'AWS')
    ], string='Tecnologia')
    years_experience = fields.Integer('Experiencia')
    
    _sql_constraints = [
        ("name_candidate_check", "UNIQUE(name,candidate_ids)", "Una candidato no puede repetir una tecnologia"),
    ]
    candidate_ids = fields.Many2one('company.candidate', string='Candidatos')
