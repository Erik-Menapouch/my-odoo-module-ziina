{
    'name': 'Website Order Notes',
    'version': '1.0',
    'category': 'Website',
    'summary': 'Add order notes field to website checkout',
    'depends': ['website_sale'],
    'data': [
    'views/checkout_note_template.xml',
    'views/sale_order_view.xml',
],
    'installable': True,
    'auto_install': False,
}
