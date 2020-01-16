from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import View
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm
from coupons.forms import CouponApplyForm


class CartView(View):

    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        for item in cart:
            item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'update': True})
        coupon_apply_form = CouponApplyForm()
        print(request.session.get('coupon_id'))
        return render(request, 'cart/detail.html', {'cart': cart, 'coupon_apply_form': coupon_apply_form})

    def post(self, request, *args, **kwargs):
        cart = Cart(request)
        product = get_object_or_404(Product, id=kwargs['product_id'])
        form = CartAddProductForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cart.add(product, quantity=cd['quantity'], update_quantity=cd['update'])
        return redirect('cart:cart_detail')


class CartDeleteItemView(View):

    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        product = get_object_or_404(Product, id=kwargs['product_id'])
        cart.remove(product)
        return redirect('cart:cart_detail')



