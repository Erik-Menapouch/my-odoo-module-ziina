from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale

class WebsiteSaleOrderNote(WebsiteSale):

    @http.route('/shop/save_note', type='http', auth='public', website=True, csrf=False)
    def save_order_note(self, customer_note='', **post):
        order = request.cart
        if order:
            order.sudo().write({'customer_note': customer_note})
        return 'ok'
