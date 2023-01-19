# -*- coding: utf-8 -*-
{
    'name': "estate",

    'summary': "Estate Property",

    'description': "Estate Property",

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
        'security/ir.model.access.csv',
        #'security/estate_property_security.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/real_estate_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
