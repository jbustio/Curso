from odoo import models,fields,api
from odoo.exceptions import UserError

class Candidate(models.Model):
    _name="recruitment.candidate"
    _description = """
    Modelo para la gestion de posibles candidatos a contratar por una empresa de desarrollo IT
    """

    _sql_constraints = [
         ('check_age','CHECK(age > 1)','The age should be positive'),
        
         
        ]

    name = fields.Char(string="Name",required=True)
    lastname = fields.Char(string="Lastname")
    ci = fields.Integer()
    address = fields.Char()
    age = fields.Integer()
    sex = fields.Selection([('Female','Female'),('Male','Male')],required=True)
    recruiter = fields.Many2one('res.partner',string="Recruiter")
    state = fields.Selection([('Pending','Pending'),
                              ('Rejected','Rejected'),
                              ('Hired','Hired')],default="Pending")
    dev_skills = fields.One2many('recruitment.tech','candidate_id',string="Technology Domained")

    def hire(self):
        if self.state == 'Pending':
            self.state = 'Sold'
        elif self.state == 'Rejected':
            raise UserError("Rejected prospect cannot be set to hired state")
        else:
            raise UserError("Hired prospect cannot be set to hired state")
    def reject(self):
        self.state = 'Rejected'
        return True
