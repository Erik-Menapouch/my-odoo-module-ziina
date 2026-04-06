import logging
import pprint

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class ZiinaController(http.Controller):

    @http.route(
        '/payment/ziina/return',
        type='http',
        auth='public',
        methods=['GET'],
        csrf=False,
        save_session=False,
    )
    def ziina_return(self, **data):
        _logger.info(
            'Ziina return received with data:\n%s',
            pprint.pformat(data)
        )
        return request.redirect('/payment/status')

    @http.route(
        '/payment/ziina/webhook',
        type='jsonrpc',
        auth='public',
        methods=['POST'],
        csrf=False,
        save_session=False,
    )
    def ziina_webhook(self, **data):
        _logger.info(
            'Ziina webhook received with data:\n%s',
            pprint.pformat(data)
        )
        return 'OK'
