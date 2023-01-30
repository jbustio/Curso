# -*- coding: utf-8 -*-
# from odoo import http


# class Company(http.Controller):
#     @http.route('/company/company', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/company/company/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('company.listing', {
#             'root': '/company/company',
#             'objects': http.request.env['company.company'].search([]),
#         })

#     @http.route('/company/company/objects/<model("company.company"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('company.object', {
#             'object': obj
#         })
