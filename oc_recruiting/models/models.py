# -*- coding: utf-8 -*-

from odoo import models, fields, api


class OcCandicate(models.Model):
    _name = 'oc.recruiting.candidate'
    _description = 'OcCandicate'

    name = fields.Char(
        compute='_compute_name')
    partner_id = fields.Many2one('res.partner', string="Candidate", copy=False,
                                 required=True
                                 )
    technology_ids = fields.One2many(
        'oc.recruiting.candidate.technology', 'candidate_id',)
    tech_ids = fields.Many2many(
        'oc.recruiting.technology', compute='_compute_tech_ids', store=True, string="Technologies")
    most_experience_technology = fields.Char(
        compute="_compute_most_experience_technology", store=True)

    most_experience = fields.Char(
        compute="_compute_most_experience")
    
    @api.depends('technology_ids')
    def _compute_most_experience(self):
        for r in self:
            mxp = max(r.technology_ids.mapped('years'))
            r.most_experience = mxp

    @api.depends('technology_ids')
    def _compute_most_experience_technology(self):
        for r in self:
            tech_ids = r.technology_ids.ids
            q = self.env['oc.recruiting.candidate.technology'].search(
                [("id", "in", tech_ids,)], order='years desc', limit=1)
            if q:
                r.most_experience_technology = f"{q.technology_id.name} {q.years} years"

    @api.depends('technology_ids.technology_id')
    def _compute_tech_ids(self):
        for r in self:
            r.tech_ids = r.technology_ids.technology_id

    @api.depends('partner_id')
    def _compute_name(self):
        for record in self:
            record.name = record.partner_id.name


class OcTechnology(models.Model):
    _name = 'oc.recruiting.technology'
    _description = "Technology"
    _order = "sequence, name"

    sql_constraints = [
        ('_unique_technology_name', 'unique (name)',
         "Technologies must be unique"),
    ]

    name = fields.Char(required=True, )
    sequence = fields.Integer(default=10)
    candidate_technology_ids = fields.One2many('oc.recruiting.candidate.technology', 'technology_id',
                                               readonly=True
                                               )


class CandidateTechnology(models.Model):
    _name = 'oc.recruiting.candidate.technology'
    _description = "Technology experience of candidates"
    # _rec_name = 'skill_id'
    _order = "years desc"

    name = fields.Char(
        compute='_compute_name')

    @api.depends('candidate_id')
    def _compute_name(self):
        for record in self:
            record.name = record.candidate_id.partner_id.name

    candidate_id = fields.Many2one(
        comodel_name='oc.recruiting.candidate',
        required=True,
        ondelete='cascade')

    technology_id = fields.Many2one(
        comodel_name='oc.recruiting.technology',
        required=True,
        ondelete='cascade')

    years = fields.Integer(string="Years", help="Years of experience.")

    sql_constraints = [
        ('_unique_tech', 'unique (candidate_id, technology_id)',
         "Can't have two experiences with the same technology"),
        ('years', 'CHECK(years BETWEEN 1 AND 50)',
         "Years should be a number between 1 and 50."),
    ]
