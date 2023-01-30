# -*- coding: utf-8 -*-

from odoo import api, models, fields, _
from odoo.exceptions import UserError, ValidationError


class CHEmployee(models.Model):
    _inherit = 'hr.employee'

    ci = fields.Char(size=11, related='address_home_id.ci', string="CI", groups="hr.group_hr_user", readonly=True)
    age = fields.Integer(related='address_home_id.age', string="Age", groups="hr.group_hr_user", readonly=True)
    sex = fields.Selection(string="Sex", related='address_home_id.sex', readonly=True)


class CHPartner(models.Model):
    _inherit = 'res.partner'
    _sql_constraints = [
        ('ci_uniq', 'UNIQUE (ci)', 'You can\'t have two employees with the same ci!'),
        ('age', 'CHECK(age >= 18)', "The age must be a positive numeric value"),
    ]

    ci = fields.Char("CI", size=11)
    age = fields.Integer("Age")
    sex = fields.Selection(string="Sex", selection=[('m', "Male"), ('f', "Female")])


class CHApplicantSkill(models.Model):

    _inherit = 'hr.applicant.skill'

    def name_get(self):
        l = []
        for record in self:
            l.append((record.id, f'{record.skill_id.name}/{record.skill_level_id.name}'))
        return l


class CHApplicant(models.Model):

    _inherit = 'hr.applicant'
    _order = "level_progress desc"

    skill_level_ids = fields.Many2many('hr.skill.level', compute='_compute_skill_level_ids', store=True)
    level_progress = fields.Integer(
        related='applicant_skill_ids.skill_level_id.level_progress')

    partner_name = fields.Char("Applicant's Full Name", compute='_compute_partner_phone_email',
                                inverse='_inverse_partner_name', store=True)

    partner_ci = fields.Char("CI", size=11, compute='_compute_partner_phone_email',
                                inverse='_inverse_partner_ci', store=True)

    partner_age = fields.Integer("Age", compute='_compute_partner_phone_email',
                                inverse='_inverse_partner_age', store=True)

    partner_sex = fields.Selection(string="Sex", selection=[('m', "Male"), ('f', "Female")],
                                   compute='_compute_partner_phone_email', inverse='_inverse_partner_sex', store=True)

    # address fields
    partner_street = fields.Char(compute="_compute_partner_address", inverse='_inverse_partner_street', store=True)
    partner_street2 = fields.Char(compute="_compute_partner_address", inverse='_inverse_partner_street2', store=True)
    partner_zip = fields.Char(compute="_compute_partner_address", change_default=True, inverse='_inverse_partner_zip', store=True)
    partner_city = fields.Char(compute="_compute_partner_address", inverse='_inverse_partner_city', store=True)
    partner_state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict',
                               domain="[('country_id', '=?', partner_country_id)]", compute="_compute_partner_address", inverse='_inverse_partner_state', store=True)
    partner_country_id = fields.Many2one('res.country', string='Country', ondelete='restrict', store=True,
                                         compute="_compute_partner_address", inverse='_inverse_partner_country')
    partner_country_code = fields.Char(related='partner_country_id.code', string="Country Code", compute="_compute_partner_address",
                                       inverse='_inverse_partner_country_code', store=True)

    # comma separated skills to style in js snippet
    full_skills_levels = fields.Text(compute="_get_full_skills_levels")

    @api.constrains('partner_age')
    def _check_partner_age(self):
        for record in self:
            # check that age is valid
            if record.partner_age and record.partner_age < 18:
                raise ValidationError(_("The partner must be at least 18 years old."))

    @api.constrains('partner_ci')
    def _check_partner_ci(self):
        for record in self:
            if record.partner_ci and len(record.partner_ci) < 11 or len(record.partner_ci) > 11:
                raise ValidationError(_("The partner ci must have eleven digits"))

            if not record.partner_ci.isnumeric():
                raise ValidationError(_("The partner ci must have eleven digits"))

    @api.depends('skill_ids')
    def _get_full_skills_levels(self):
        for record in self:
            record.full_skills_levels = ','.join([f'{sk.name_get()[0][1]}' for sk in record.applicant_skill_ids])

    @api.depends('applicant_skill_ids.skill_level_id')
    def _compute_skill_level_ids(self):
        for applicant in self:
            applicant.skill_level_ids = applicant.applicant_skill_ids.skill_level_id

    @api.depends('partner_id', 'partner_id.name', 'partner_id.email', 'partner_id.mobile', 'partner_id.phone',
                 'partner_id.ci', 'partner_id.age', 'partner_id.sex')
    def _compute_partner_phone_email(self):
        for applicant in self:
            applicant.partner_name = applicant.partner_id.name
            applicant.partner_phone = applicant.partner_id.phone
            applicant.partner_ci = applicant.partner_id.ci
            applicant.partner_age = applicant.partner_id.age
            applicant.partner_sex = applicant.partner_id.sex
            applicant.partner_mobile = applicant.partner_id.mobile
            applicant.email_from = applicant.partner_id.email

    @api.depends('partner_id', 'partner_id.street', 'partner_id.street2', 'partner_id.city',
                 'partner_id.zip', 'partner_id.state_id', 'partner_id.country_id', 'partner_id.country_code')
    def _compute_partner_address(self):
        for applicant in self:
            applicant.partner_street = applicant.partner_id.street
            applicant.partner_street2 = applicant.partner_id.street2
            applicant.partner_zip = applicant.partner_id.zip
            applicant.partner_city = applicant.partner_id.city
            applicant.partner_state_id = applicant.partner_id.state_id
            applicant.partner_country_id = applicant.partner_id.country_id
            applicant.partner_country_code = applicant.partner_id.country_code

    def _inverse_partner_name(self):
        for applicant in self.filtered(lambda a: a.partner_id and a.partner_name):
            applicant.partner_id.name = applicant.partner_name

    def _inverse_partner_ci(self):
        for applicant in self.filtered(lambda a: a.partner_id and a.partner_ci):
            applicant.partner_id.ci = applicant.partner_ci

    def _inverse_partner_age(self):
        for applicant in self.filtered(lambda a: a.partner_id and a.partner_age):
            applicant.partner_id.age = applicant.partner_age

    def _inverse_partner_sex(self):
        for applicant in self.filtered(lambda a: a.partner_id and a.partner_sex):
            applicant.partner_id.sex = applicant.partner_sex

    def _inverse_partner_street(self):
        for applicant in self.filtered(lambda a: a.partner_id and a.partner_street):
            applicant.partner_id.street = applicant.partner_street

    def _inverse_partner_street2(self):
        for applicant in self.filtered(lambda a: a.partner_id and a.partner_street2):
            applicant.partner_id.street2 = applicant.partner_street2

    def _inverse_partner_zip(self):
        for applicant in self.filtered(lambda a: a.partner_id and a.partner_zip):
            applicant.partner_id.zip = applicant.partner_zip

    def _inverse_partner_city(self):
        for applicant in self.filtered(lambda a: a.partner_id and a.partner_city):
            applicant.partner_id.city = applicant.partner_city

    def _inverse_partner_state(self):
        for applicant in self.filtered(lambda a: a.partner_id and a.partner_state_id):
            applicant.partner_id.state_id = applicant.partner_state_id

    def _inverse_partner_country(self):
        for applicant in self.filtered(lambda a: a.partner_id and a.partner_country_id):
            applicant.partner_id.country_id = applicant.partner_country_id

    def _inverse_partner_country_code(self):
        for applicant in self.filtered(lambda a: a.partner_id and a.partner_country_code):
            applicant.partner_id.country_code = applicant.partner_country_code

    def create_employee_from_applicant(self):
        """ Create an employee from applicant """
        self.ensure_one()
        self._check_interviewer_access()

        contact_name = False
        if self.partner_id:
            address_id = self.partner_id.address_get(['contact'])['contact']
            contact_name = self.partner_id.display_name
        else:
            if not self.partner_name:
                raise UserError(_('You must define a Contact Name for this applicant.'))
            new_partner_id = self.env['res.partner'].create({
                'is_company': False,
                'type': 'private',
                'name': self.partner_name,
                'email': self.email_from,
                'phone': self.partner_phone,
                'mobile': self.partner_mobile,
                'ci': self.partner_ci,
                'age': self.partner_age,
                'sex': self.partner_sex,

            })
            self.partner_id = new_partner_id
            address_id = new_partner_id.address_get(['contact'])['contact']
        employee_data = {
            'default_name': self.partner_name or contact_name,
            'default_job_id': self.job_id.id,
            'default_job_title': self.job_id.name,
            'default_address_home_id': address_id,
            'default_department_id': self.department_id.id,
            'default_address_id': self.company_id.partner_id.id,
            'default_work_email': self.department_id.company_id.email,
            'default_work_phone': self.department_id.company_id.phone,
            'form_view_initial_mode': 'edit',
            'default_applicant_id': self.ids,
        }
        dict_act_window = self.env['ir.actions.act_window']._for_xml_id('hr.open_view_employee_list')
        dict_act_window['context'] = employee_data
        return dict_act_window

