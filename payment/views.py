import braintree
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from orders.models import Order


class PaymentView(View):

    def get(self, request):
        order_id = request.session.get('order_id')
        order = get_object_or_404(Order, id=order_id)
        client_token = braintree.ClientToken.generate()
        return render(request, 'payment/process.html', {'order': order, 'client_token': client_token})

    def post(self, request):
        order_id = request.session.get('order_id')
        order = get_object_or_404(Order, id=order_id)
        nonce = request.POST.get('payment_method_nonce', None)
        result = braintree.Transaction.sale({
            'amount': f'{order.get_total_cost()}',
            'payment_method_nonce': nonce,
            'options': {
                'submit_for_settlement': True
            }
        })
        if result.is_success:
            order.paid = True
            order.braintree_id = result.transaction.id
            order.save()
            return redirect('payment:done')
        else:
            return redirect('payment:canceled')


def payment_done(request):
    request.session['coupon_id'] = None
    return render(request, 'payment/done.html')


def payment_canceled(request):
    return render(request, 'payment/canceled.html')
