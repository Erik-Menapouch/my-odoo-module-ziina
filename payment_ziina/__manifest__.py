{
    'name': 'Ziina Payment Provider',
    'version': '1.0',
    'category': 'Accounting/Payment Providers',
    'summary': 'Ziina Payment Gateway for Odoo',
    'author': 'Erik Menapouch',
    'depends': ['payment'],
    'data': [
        'views/payment_ziina_templates.xml',
    ],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
