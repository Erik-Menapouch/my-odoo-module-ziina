import logging
import requests

from odoo import fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

ZIINA_API_URL = 'https://api-v2.ziina.com/api/payment_intent'


class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(
        selection_add=[('ziina', 'Ziina')],
        ondelete={'ziina': 'set default'}
    )
    ziina_api_key = fields.Char(
        string='Ziina API Key',
        required_if_provider='ziina',
    )

    def _ziina_get_headers(self):
        return {
            'Authorization': f'Bearer {self.ziina_api_key}',
            'Content-Type': 'application/json',
        }

    def _get_default_payment_method_codes(self):
        default_codes = super()._get_default_payment_method_codes()
        if self.code != 'ziina':
            return default_codes
        return ['ziina']


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    def _get_specific_rendering_values(self, processing_values):
        res = super()._get_specific_rendering_values(processing_values)
        if self.provider_code != 'ziina':
            return res

        provider = self.provider_id
        base_url = self.provider_id.get_base_url()

        payload = {
            'amount': int(self.amount * 100),
            'currency_code': self.currency_id.name,
            'message': self.reference,
            'success_url': f'{base_url}/payment/ziina/return?ref={self.reference}',
            'cancel_url': f'{base_url}/payment/ziina/return?ref={self.reference}',
            'test': self.provider_id.state == 'test',
        }

        try:
            response = requests.post(
                ZIINA_API_URL,
                json=payload,
                headers=provider._ziina_get_headers(),
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()
            self.provider_reference = data.get('id')
            redirect_url = data.get('redirect_url')
            return {
                'api_url': redirect_url,
                'form_html': f'<form id="ziina_redirect_form" action="{redirect_url}" method="get"></form>',
            }
        except Exception as e:
            _logger.error('Ziina payment error: %s', str(e))
            raise ValidationError('Could not connect to Ziina. Please try again.')
