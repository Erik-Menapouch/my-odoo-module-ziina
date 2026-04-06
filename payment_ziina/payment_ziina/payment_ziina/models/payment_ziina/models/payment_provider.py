import requests
import logging

from odoo import fields, models

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
