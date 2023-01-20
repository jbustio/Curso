# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Estate Property',
    'version': '15.0.1',
    'summary': 'Mi Estate Property ',
    'sequence': 10,
    'description': """
    My Estate Property
    """,
    'category': 'Estate',
    'website': 'https://www.odoo.com/app/estate_property',
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_view.xml',
        'views/estate_property_type_view.xml',
        'views/estate_property_tax_view.xml',
        'views/estate_property_menu.xml',
        'views/estate_property_offer.xml',
        'security/estate_property_security.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
