/** @odoo-module **/
import { PaymentForm } from '@payment/js/payment_form';
import { patch } from '@web/core/utils/patch';

patch(PaymentForm.prototype, {
    async _processRedirectFlow(providerCode, paymentOptionId, flowCode, processingValues) {
        if (providerCode !== 'ziina') {
            return super._processRedirectFlow(...arguments);
        }
        window.location = processingValues.api_url;
    },
});
