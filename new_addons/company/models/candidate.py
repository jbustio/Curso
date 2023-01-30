from odoo import fields, models, api
from odoo.exceptions import ValidationError

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
    #technology_ids = fields.Many2many('company.technology', 'candidate_technology','candidate_id','technology_id' , string='Tecnologias')
    candidate_technology_ids = fields.One2many('candidate.technology','candidate_id' ,string='candidate_technology',auto_join=True)
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
    _sql_constraints = [
        ("name_check", "UNIQUE(name)", "Las tecnologias son unicas en la empresa"),
    ]
    candidate_ids = fields.Many2many('company.candidate','candidate_technology','technology_id','candidate_id', string='Candidatos')
    

class CandidateTechnologyRel(models.Model):
    _name = 'candidate.technology'
    _description = 'CandidateTechnologyRel'
    _rec_name = 'candidate_id'
    _order = 'technology_id years_experience'
   
    candidate_id = fields.Many2one('company.candidate',string='candidate', ondelete='cascade', required=True, index=True)
    technology_id = fields.Many2one('company.technology' , string='technology',ondelete='cascade',required=True, index=True)
    years_experience = fields.Integer('Experiencia')
