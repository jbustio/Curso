# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class OcCandicate(models.Model):
    _name = 'oc.recruiting.candidate'
    _description = 'OcCandicate'

    name = fields.Char(
        compute='_compute_name', inverse='_inverse_name')
    partner_id = fields.Many2one('res.partner', string="Candidate", copy=False,
                                 required=True
                                 )
    technology_ids = fields.One2many(
        'oc.recruiting.candidate.technology', 'candidate_id', required=True)
    tech_ids = fields.Many2many(
        'oc.recruiting.technology', compute='_compute_tech_ids', store=True, string="Technologies")
    most_experience_technology = fields.Char(
        compute="_compute_most_experience_technology", store=True)

    accept = fields.Boolean(default=False)
    
    state = fields.Selection(required=True, default="new", copy=False, tracking=True,
                             selection=[('new', 'New Candidate'), ('accepted', 'Accepted Candidate'), (
                                 'employee', 'Employee'), ('refuse', 'Refused Candidate'),])
    employee_id = fields.Many2one(
        'hr.employee', string='Employee', index=True, tracking=True)

    tech_count = fields.Integer(compute='_compute_tech_count', store=True)
    
    @api.depends('technology_ids')
    def _compute_tech_count(self):
        for record in self:
            record.tech_count = len(record.technology_ids.ids) 

    def _inverse_name(self):
        for record in self:
            record.partner_id.name = record.name

    def _inverse_last_name(self):
        for record in self:
            record.partner_id.last_name = record.last_name

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

    def action_make_employee(self):
        for record in self:
            record.state = "employee"
            employee = self.env['hr.employee'].create({
                "user_partner_id": record.partner_id.id,
                "name": record.partner_id.name,
            })
            record.employee_id = employee
       
    def most_experience_btn(self):
        pass

    def action_refuse(self):
        for record in self:
            record.state = "refuse"

    @api.onchange("accept")
    def _onchange_accept(self):
        for record in self:
            if record.state in ["new", "accepted"] and record.tech_ids.ids:
                record.state = "accepted" if record.accept else "new"

    @api.model
    def create(self, vals):
        if not vals.get("technology_ids", None):
            raise UserError(_("At leat one technology should be added"))
        return super().create(vals)



class OcTechnology(models.Model):
    _name = 'oc.recruiting.technology'
    _description = "Technology"
    _order = "sequence, name"

    _sql_constraints = [
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

    years = fields.Integer(string="Years of XP", help="Years of experience.")

    _sql_constraints = [
        ('_unique_tech', 'unique (candidate_id, technology_id)',
         "Can't have two experiences with the same technology"),
        ('years', 'CHECK(years BETWEEN 1 AND 50)',
         "Years should be a number between 1 and 50."),
    ]
