import json
from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale

class WebsiteSaleOrderNote(WebsiteSale):

    @http.route('/shop/checkout', type='http', auth='public', website=True)
    def shop_checkout(self, try_skip_step=None, **post):
        return super(WebsiteSaleOrderNote, self).shop_checkout(try_skip_step=try_skip_step, **post)

    @http.route('/shop/address', type='http', auth='public', website=True, sitemap=False)
    def shop_address_submit(self, **post):
        if post.get('customer_note') is not None:
            order = request.website.sale_get_order()
            if order:
                order.sudo().write({
                    'customer_note': post.get('customer_note', '')
                })
        return super(WebsiteSaleOrderNote, self).shop_address_submit(**post)
