# -*- coding: utf-8 -*-
{
    'name': "company",

    'summary': """
        Company of developers""",

    'description': """
        Company of developers
    """,

    'author': "Richar",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        #'security/ir.model.access.csv',
        #'security/company_security.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/candidate_view.xml',
        'views/technology_view.xml',
        'report/technology_report.xml',
        'report/technology_template.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
