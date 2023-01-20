# -*- coding: utf-8 -*-
{
    'name': "real_estate",

    'summary': """
        Modulo sobre el manejo de bienes raices""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Dariel",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Services/Library',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        
        
        'security/ir.model.access.csv',
        'security/real_estate_security.xml',
        'security/type_security.xml',
        'security/tag_security.xml',
        'security/offer_security.xml',
        'views/real_estate_view.xml',
        'views/real_estate_menu.xml',
        'views/estate_type_menu.xml',
        'views/estate_type_view.xml',
        'views/estate_tag_view.xml',
        'views/estate_offer_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'license': 'LGPL-3',
    'application':False,
}
