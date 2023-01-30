from odoo import models,fields,api

class Tech(models.Model):
    _name = "recruitment.tech"
    _description = """
    Modelo para la gestion de las tecnologias que dominan los candidatos
    """
    name= fields.Selection([
        ('Angular','Angular'),
        ('Vue','Vue'),
        ('React Native','React Native'),
        ('CSS','CSS'),
        ('HTML','HTML'),
        ('Sprintboot','Sprintboot'),
        ('Odoo','Odoo'),
        ('React','React'),
        ('Flutter','Flutter'),
        ('Python','Python'),
        ('AWS','AWS')],string="Technologies",required=True)
    years_experience=fields.Integer(string="Years of use")
    candidate_id=fields.Many2one('recruitment.candidate',string="Candidate")