-*- coding: utf-8 -*-
from odoo import http


class Company(http.Controller):
    @http.route("/", auth="public")
    def list(self, **kw):
        return http.request.render('company.candidate', {
            'root': '/',
            'objects': http.request.env['company.candidate'].search([]),
        })
