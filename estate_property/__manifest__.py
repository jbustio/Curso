{
    'name' : 'Estate Property',
    'description':""" ... """,
    'version' : '1.0',
    'author': 'Dayron',
    'depends' : ['base'],
    'data': [
        'views/estate_property.xml',
        'views/property_type.xml',
        'views/property_tag.xml',
        ],
    'application': False, #Remember: Just use this parameter when you are sure that what you are importing is a full flesh app, otherwise is just a module by default 
}