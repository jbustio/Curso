{
    'name' : 'Real Estate',
    'description':""" ... """,
    'version' : '1.0',
    'author': 'Dayron',
    'depends' : ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property.xml',
        'views/property_type.xml',
        'views/property_tag.xml',
        'views\property_offer.xml'
        ],
    'application': False, #Remember: Just use this parameter when you are sure that what you are importing is a full flesh app, otherwise is just a module by default 
}