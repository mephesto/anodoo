# -*- coding: utf-8 -*-
{
    'name': "交互渠道-会议",

    'summary': """
        会议交互,通过线上,线下会议等形式和客户交互
    """,

    'description': """
        会议交互,通过线上,线下会议等形式和客户交互
    """,

    'author': "Anodoo",
    'website': "http://www.anodoo.com/module/anodoo-engage-meeting",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Anodoo',
    'version': '13.1',
    'application': False,
    'installable': True,

    # any module necessary for this one to work correctly
    'depends': ['anodoo_base', 'anodoo_engage', 'anodoo_mktauto'],

    # always loaded
    'data': [
        'data/engage_meeting_data.xml',
        'security/engage_meeting_security.xml',
        'security/ir.model.access.csv',
        'views/engage_meeting_views.xml',
        'views/engage_meeting_menu.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}