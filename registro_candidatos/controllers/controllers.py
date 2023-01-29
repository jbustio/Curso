# -*- coding: utf-8 -*-
# from odoo import http


# class RegistroCandidatos(http.Controller):
#     @http.route('/registro_candidatos/registro_candidatos', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/registro_candidatos/registro_candidatos/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('registro_candidatos.listing', {
#             'root': '/registro_candidatos/registro_candidatos',
#             'objects': http.request.env['registro_candidatos.registro_candidatos'].search([]),
#         })

#     @http.route('/registro_candidatos/registro_candidatos/objects/<model("registro_candidatos.registro_candidatos"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('registro_candidatos.object', {
#             'object': obj
#         })
