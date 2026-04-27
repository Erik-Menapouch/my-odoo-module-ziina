from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale

class WebsiteSaleOrderNote(WebsiteSale):

    @http.route('/shop/checkout', type='http', auth='public', website=True)
    def checkout(self, **post):
        if post.get('customer_note') is not None:
            order = request.website.sale_get_order()
            if order:
                order.sudo().write({
                    'customer_note': post.get('customer_note', '')
                })
        return super().checkout(**post)
