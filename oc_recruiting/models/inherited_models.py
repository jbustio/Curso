from odoo import models, fields, api


class OcRespartner(models.Model):
    _inherit = 'res.partner'

    # Nombre y Apellidos, CI, dirección actual, edad y sexo
    last_name = fields.Char()
    ci = fields.Char(
        size=11
    )
    current_address = fields.Char()
    age = fields.Integer()
    sex = fields.Selection([('m', 'Man'), ('f', 'Woman')], default="f")

class OcEmployee(models.Model):

    _inherit = "hr.employee"
    # personal_information
    candidate_ids = fields.One2many('oc.recruiting.candidate', 'employee_id')
    tech_ids = fields.Many2many('oc.recruiting.candidate.technology',  compute='_compute_tech_ids', store=True, string="Technologies")
  

    @api.depends('candidate_ids')
    def _compute_tech_ids(self):
        for r in self:
            r.tech_ids = r.candidate_ids.technology_ids
