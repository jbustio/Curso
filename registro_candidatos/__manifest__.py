# -*- coding: utf-8 -*-
{
    'name': "registro_candidatos",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'contacts', 'website'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/menu_views.xml',
        'views/inherit_candidate.xml',
        'views/technology.xml',
        'views/register.xml',
        'report/tech_report.xml',
        'views/snippet.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'assets': {
        'website.assets_frontend': [
            'registro_candidatos/static/src/js/list_snipper.js',
        ],
    },
    # web.assets_common, web.assets_backend and website.assets_frontend
}
