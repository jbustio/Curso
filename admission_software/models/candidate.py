from odoo import fields, models, api , exceptions




class Candidate(models.Model):
    _description = 'Candidates to admission'
    _name = 'candidate'
    
    _sql_constraints = [
        (
            'check_age', 
            'CHECK(age >= 18)',
            'The candidate must be an adult to aply.'
        )
    ]

    name = fields.Char(string = "Name", required  =True)
    lastname = fields.Char(string = "Last Name")
    ci= fields.Char(string  = "Identitiy Number",size=11, required  = True)
    
    address = fields.Text(string  ="Address")
    cv = fields.Text(string = "C.V")
    sex =  fields.Selection( [('Male','Male'),('Female','Female'),('Non-Binary','Non-Binary')], string = "Sex" )
    age = fields.Integer(string = "Age",required=True, default = 18)
    
    interviewer = fields.Many2one('res.partner',string="Interviewer", default=lambda self: self.env.user)
    recruiter = fields.Many2one('res.users', string='Recruiter', readonly=True )
    
    state = fields.Selection([('Hired','Hired'),('On Hold','On Hold'),('Refused','Refused')])
    
    technologies_ids = fields.One2many('technology.experience','candidate_id',string="Technology Experience")
    
    @api.constrains("ci")
    def _check_ci(self):
        for record in self:
            if (len(record.ci) != 11):
                raise exceptions.UserError("The identification must be 11 digits")
            
            try:
                int(record.ci)
            except ValueError:
                raise exceptions.UserError("The identification must be a number")
                
            
            
    def action_hire(self):
        for record in self:
            if record.state == 'Hired':
                raise exceptions.UserError("Only candidates on hold can be hired")
            record.state = 'Hired'
            record.recruiter = self.env.user

    def action_refuse(self):
        for record in self:
            if record.state == 'Refused' or record.state == 'Hired' :
                raise exceptions.UserError("Only candidates on hold can be refused")
            record.state = 'Refused'
            
    