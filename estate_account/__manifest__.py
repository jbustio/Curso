{
    'name': "estate.account",

    'summary': """
        Modulo sobre el manejo de cuentas""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Dariel",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Real Estate/',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base_setup','real_estate','account'],

    # always loaded
    'data': [
        
        
        
        
        'security/ir.model.access.csv',
        'views/estate_account_menu.xml',
        
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'license': 'LGPL-3',
    'application':False,
}
