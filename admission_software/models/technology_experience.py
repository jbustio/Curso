from odoo import fields, models, Command, api
from odoo.exceptions import UserError




class TechnologyExperience(models.Model):
    _description = 'Experience of a candidate with especific technologies'
    _name = 'technology.experience'
    
    _order="experience desc"
    
    
    technology_name= fields.Selection([('Angular','Angular'),('Vue','Vue'),('React Native','React Native'),
                            ('CSS','CSS'),('Sprintboot','Sprintboot'),('Odoo','Odoo'),('React','React'),
                            ('Flutter','Flutter'),('Python','Python'),('HTML','HTML'),('AWS','AWS')],
                           string="Technologies",required=True)
    
    experience=fields.Integer(string="Years of Expirience",required= True, default = 1)
    candidate_id=fields.Many2one('candidate',string="Candidate")
    
    notes = fields.Text("Notes")
    
    @api.constrains("name")
    def _check_duplicate(self):
        for record in self:
            if record.search_count([('technology_name','=','self')]) > 1:
                raise UserError("Technologies can't be duplicated")