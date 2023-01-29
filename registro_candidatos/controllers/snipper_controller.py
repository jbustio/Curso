# -*- coding: utf-8 -*-
from odoo import http


class ListSnipper(http.Controller):
    @http.route("/list_candidate_tech", type="json", auth="public", method=["POST"], website=True)
    def get_tecnologies(self):
        tech = http.request.env["register.candidate"].sudo().search_read([], ["candidate_id", "tech_id", "experience"])
        return tech
