{
    'name':'recruitment.candidate',

    'summary':"""
    Final exercise of the Countigo odoo 's course
    """,

    'author':'Dariel',

    'category':'Recruitment/',
    'version':'0.1',
    'depends':['base','website'],

    'data': [
        'security/candidate_security.xml',
        'security/tech_security.xml',
        'security/ir.model.access.csv',
        
        'views/tech_view.xml',
        'views/recruitment_view.xml',
        'views/recruitment_menu.xml',
        'views/candidates_list_template.xml',
        'views/snippets.xml',
        'reports/candidates_printpdf_action.xml',
        'reports/candidates_pdf_template.xml'
        
    ],
    'assets':{
        'website.assets_frontend':{
            "recruitment_candidate/static/src/css/candidate.css",
            "recruitment_candidate/static/src/js/candidate.js",
            "recruitment_candidate/static/src/snippet.js",
        }
    },
    'license':'LGPL-3',
    'application':True
}