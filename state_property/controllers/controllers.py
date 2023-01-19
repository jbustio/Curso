# -*- coding: utf-8 -*-
# from odoo import http


# class StateProperty(http.Controller):
#     @http.route('/state_property/state_property', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/state_property/state_property/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('state_property.listing', {
#             'root': '/state_property/state_property',
#             'objects': http.request.env['state_property.state_property'].search([]),
#         })

#     @http.route('/state_property/state_property/objects/<model("state_property.state_property"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('state_property.object', {
#             'object': obj
#         })
