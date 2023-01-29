# -*- coding: utf-8 -*-
# from odoo import http


# class CustomRecruitment(http.Controller):
#     @http.route('/custom_recruitment/custom_recruitment', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/custom_recruitment/custom_recruitment/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('custom_recruitment.listing', {
#             'root': '/custom_recruitment/custom_recruitment',
#             'objects': http.request.env['custom_recruitment.custom_recruitment'].search([]),
#         })

#     @http.route('/custom_recruitment/custom_recruitment/objects/<model("custom_recruitment.custom_recruitment"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('custom_recruitment.object', {
#             'object': obj
#         })
