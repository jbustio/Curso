# -*- coding: utf-8 -*-
# from odoo import http


# class EzRecruiting(http.Controller):
#     @http.route('/ez_recruiting/ez_recruiting', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ez_recruiting/ez_recruiting/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('ez_recruiting.listing', {
#             'root': '/ez_recruiting/ez_recruiting',
#             'objects': http.request.env['ez_recruiting.ez_recruiting'].search([]),
#         })

#     @http.route('/ez_recruiting/ez_recruiting/objects/<model("ez_recruiting.ez_recruiting"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ez_recruiting.object', {
#             'object': obj
#         })
