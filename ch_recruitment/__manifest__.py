# -*- coding: utf-8 -*-
{
    'name': "Advanced Recruitment",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Jesus Cobacho Aguilera",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['website', 'hr_recruitment_skills'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/snippets.xml',
        'views/applicant_search_view.xml',
        'views/applicant_tree_view_job.xml',
        'views/partner_view_form_private.xml',
        'views/views.xml'

    ],
    'demo': [
        'demo/demo.xml'
    ],
    'assets': {
        'web.assets_frontend': [
            '/ch_recruitment/static/src/js/snippets.js'
        ]
    },
    "application": True,

}
