# -*- coding: utf-8 -*-
# from odoo import http


# class Applicants(http.Controller):
#     @http.route('/applicants/applicants', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/applicants/applicants/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('applicants.listing', {
#             'root': '/applicants/applicants',
#             'objects': http.request.env['applicants.applicants'].search([]),
#         })

#     @http.route('/applicants/applicants/objects/<model("applicants.applicants"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('applicants.object', {
#             'object': obj
#         })
