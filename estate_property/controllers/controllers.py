# -*- coding: utf-8 -*-
from odoo import http


class EstateProperty(http.Controller):
    @http.route('/estate_property/estate_property', auth='public')
    def index(self, **kw):
        return "Hello, world"

    @http.route('/estate_property/estate_property/objects', auth='public')
    def list(self, **kw):
        return http.request.render('estate_property.listing', {
            'root': '/estate_property/estate_property',
            'objects': http.request.env['estate_property.estate_property'].search([]),
        })

    @http.route('/estate_property/estate_property/objects/<model("estate_property.estate_property"):obj>', auth='public')
    def object(self, obj, **kw):
        return http.request.render('estate_property.object', {
            'object': obj
        })
