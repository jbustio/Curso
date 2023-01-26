from odoo import http

class ControllerName(http.Controller):
    """ The summary line for a class docstring should fit on one line.

        Routes:
          /some_url: url description
    """

    @http.route('/some_url', type='http', auth='none')
    def some_url(self, **kw):

        pass
