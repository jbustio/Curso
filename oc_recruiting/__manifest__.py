# -*- coding: utf-8 -*-
{
    'name': "OC Recruiting",
    'summary': """
        Final task for the odoo curse""",

    'description': """
        Long description of module's purpose
    """,
    'author': "Osvaldo Cobacho Aguilera",
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr_recruitment', 'hr_skills'],
    'data': [
        'security/ir.model.access.csv',
        'reports/oc_recruiting_templates.xml',
        'reports/oc_recruiting_reports.xml',
        'views/hr_skills.xml',
        'views/technology_views.xml',
        'views/candidate_views.xml',
        'views/candidate_technologies_views.xml',
        'views/candidate_technology_experience_views.xml',
        'views/views.xml',
        'views/menu.xml',

    ],
    'demo': ['demo/demo.xml', ],
}
