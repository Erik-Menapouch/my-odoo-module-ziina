from odoo import models, fields

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    customer_note = fields.Text(
        string='Order Notes',
        help='Customer notes for this order (e.g. mix pack flavor choices)'
    )
