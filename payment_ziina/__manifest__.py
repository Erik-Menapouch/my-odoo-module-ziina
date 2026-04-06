{
    'name': 'Ziina Payment Provider',
    'version': '1.0',
    'category': 'Accounting/Payment Providers',
    'summary': 'Ziina Payment Gateway for Odoo',
    'author': 'Erik Menapouch',
    'depends': ['payment'],
    'data': [
        'data/payment_provider.xml',
        'data/payment_method.xml',
        'views/payment_ziina_templates.xml',
        'views/assets.xml',
    ],
    'assets': {
        'web.assets_frontend_lazy': [
            'payment_ziina/static/src/js/payment_form.js',
        ],
    },
    'post_init_hook': 'post_init_hook',
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
