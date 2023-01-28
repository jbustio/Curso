from odoo import models,fields,api


class Candidate(models.Model):
    _name="recruitment.candidate"
    _description = """
    Modelo para la gestion de posibles candidatos a contratar por una empresa de desarrollo IT
    """

    name = fields.Char(string="Name")