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
        _logger.info('Ziina return received with data:\n%s', pprint.pformat(data))
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
        _logger.info('Ziina webhook received with data:\n%s', pprint.pformat(data))
        try:
            payload = request.get_json_data()
        except Exception:
            payload = data
        _logger.info('Ziina webhook payload:\n%s', pprint.pformat(payload))

        # Handle nested payload from Ziina
        if 'data' in payload:
            payload = payload['data']

        payment_intent_id = payload.get('id')
        status = payload.get('status')

        _logger.info('Processing payment intent %s with status %s', payment_intent_id, status)

        if payment_intent_id and status:
            tx = request.env['payment.transaction'].sudo().search(
                [('provider_reference', '=', payment_intent_id)], limit=1
            )
            if tx:
                _logger.info('Found transaction %s', tx.reference)
                if status == 'completed':
                    tx._set_done()
                elif status == 'failed':
                    tx._set_error('Payment failed on Ziina')
                elif status == 'cancelled':
                    tx._set_canceled()
            else:
                _logger.warning('No transaction found for payment intent %s', payment_intent_id)
        return 'OK'
