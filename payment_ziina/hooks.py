import logging

_logger = logging.getLogger(__name__)


def post_init_hook(env):
    """Create Ziina payment method and link it to the provider."""
    method = env['payment.method'].search([('code', '=', 'ziina')], limit=1)
    if not method:
        method = env['payment.method'].create({
            'name': 'Ziina',
            'code': 'ziina',
            'active': True,
        })
    provider = env['payment.provider'].search([('code', '=', 'ziina')], limit=1)
    if provider and method:
        provider.write({'payment_method_ids': [(4, method.id)]})
