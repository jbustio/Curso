from odoo import http
from odoo.http import request


""" class Main(http.Controller):
    @http.route('/estate/hello_world',type='http', auth='public')
    def index(self):
        estate_properties = request.env['real_estate'].sudo().search([])
        html_result = '<html><body><ul>'
        for property in estate_properties:
            html_result += "<li> %s </li>" % property.name
            html_result += "</ul></body></html>"
        return html_result """