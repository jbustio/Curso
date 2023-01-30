from odoo import models,fields,api
from odoo.exceptions import UserError


class Tech(models.Model):
    _name = "recruitment.tech"
    _description = """
    Modelo para la gestion de las tecnologias que dominan los candidatos
    """
    _order="years_experience desc"

    

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

    @api.constrains("name")
    def _check_duplicate(self):
        for record in self:
            if record.search_count([('name','=','self')]) > 1:
                raise UserError("You only can select a technology once")