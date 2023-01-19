# -*- coding: utf-8 -*-
# from odoo import http


# class RealEstate(http.Controller):
#     @http.route('/real_estate/real_estate', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/real_estate/real_estate/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('real_estate.listing', {
#             'root': '/real_estate/real_estate',
#             'objects': http.request.env['real_estate.real_estate'].search([]),
#         })

#     @http.route('/real_estate/real_estate/objects/<model("real_estate.real_estate"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('real_estate.object', {
#             'object': obj
#         })
