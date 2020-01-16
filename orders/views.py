from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .forms import OrderCreateForm
from .models import OrderItem, Order
from cart.cart import Cart
from .tasks import order_created
from django.views.generic import View
from django.contrib.admin.views.decorators import staff_member_required


class OrderView(View):
    form_class = OrderCreateForm

    def get(self, request):
        cart = Cart(request)
        form = self.form_class()
        return render(request, 'orders/order/create.html', {'cart': cart, 'form': form})

    def post(self, request):
        cart = Cart(request)
        form = self.form_class(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            cart.clear()
            order_created.delay(order.id)
            request.session['order_id'] = order.id
            return redirect(reverse('payment:process'))


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'admin/orders/order/detail.html', {'order': order})
