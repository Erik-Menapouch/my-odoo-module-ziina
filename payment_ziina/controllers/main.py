import logging
import pprint
import requests
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
        type='json',
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

        if 'data' in payload:
            payload = payload['data']

        payment_intent_id = payload.get('id')
        status = payload.get('status')

        _logger.info('Processing payment intent %s with status %s', payment_intent_id, status)

        if payment_intent_id:
            provider = request.env['payment.provider'].sudo().search(
                [('code', '=', 'ziina')], limit=1
            )
            if provider:
                try:
                    api_key = provider.sudo().read(['ziina_api_key'])[0].get('ziina_api_key', '')
                    response = requests.get(
                        f'https://api-v2.ziina.com/api/payment_intent/{payment_intent_id}',
                        headers={'Authorization': f'Bearer {api_key}'},
                        timeout=10
                    )
                    if response.status_code == 200:
                        actual_data = response.json()
                        status = actual_data.get('status', status)
                        _logger.info('Actual status from Ziina API: %s', status)
                except Exception as e:
                    _logger.warning('Could not fetch status from Ziina API: %s', e)

            tx = request.env['payment.transaction'].sudo().search(
                [('provider_reference', '=', payment_intent_id)], limit=1
            )
            if tx:
                _logger.info('Found transaction %s', tx.reference)
                if status == 'completed':
                    tx._set_done()
                    journal = tx.provider_id.journal_id
                    online_line = journal.inbound_payment_method_line_ids.filtered(
                        lambda l: l.payment_method_id.code == 'online'
                    )
                    if online_line:
                        tx.with_context(payment_method_line_id=online_line.id)._post_process()
                    else:
                        tx._post_process()
                elif status == 'failed':
                    tx._set_error('Payment failed on Ziina')
                elif status == 'cancelled':
                    tx._set_canceled()
            else:
                _logger.warning('No transaction found for payment intent %s', payment_intent_id)
        return 'OK'
