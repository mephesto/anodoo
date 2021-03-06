# -*- coding: utf-8 -*-
{
    'name': "团队协同",

    'summary': """
        团队协同
    """,

    'description': """
        团队协同
    """,

    'author': "Anodoo",
    'website': "http://www.anodoo.com/module/anodoo-team",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Anodoo',
    'version': '13.1',
    'application': True,
    'installable': True,

    # any module necessary for this one to work correctly
    'depends': ['anodoo_base', 'sales_team'],

    # always loaded
    'data': [
        'data/team_data.xml',
        'security/team_security.xml',
        'security/ir.model.access.csv',
        'views/team_views.xml',
        'views/team_menu.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}