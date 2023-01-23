{
'name':'Real State Advertisement',
'summary': "Promote avaliable home for buying",
'description': """
Advertisement Module
====================
Promote your house sale proposition to the world in order to build a brand, attract clients, and close real estate transactions.
""",
'author': "Niorlys",
'website': "",
'category': 'Sales/Property',
'depends': ['base'],
'version': '13.0.1',
'data': [
    'security/rea_security_groups.xml',
    'security/ir.model.access.csv',
    'views/estate_property_views.xml',
    'views/property_type_views.xml' # We use as base menu item created in estate_property_view
],
"license": "AGPL-3",
"application": True,
}
