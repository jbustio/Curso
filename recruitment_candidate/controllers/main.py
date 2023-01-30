from odoo import http

class Candidates(http.Controller):
    @http.route("/candidates",auth="public",website=True)
    def list(self, **kwargs):
        Candidate = http.request.env["recruitment.candidate"]
        cands = Candidate.search([])
        return http.request.render(
            "recruitment_candidate.candidates_list_template",
            {"cands":cands}
        ) 