from odoo import http 

class Main(http.Controller): 
    @http.route("/", auth="public", website=True)
    def catalog(self, **kwargs): 
        Candidate = http.request.env["oc.recruiting.candidate"]
        print(http.request.params)
        search = http.request.params.get("search", "")
        domain = []
        if search:
            domain = [("partner_id.name","ilike", search )]
        candidates = Candidate.sudo().search(domain, order="most_experience_technology desc") 
        return http.request.render( "oc_recruiting_portal.candidates", {"candidates": candidates}, )