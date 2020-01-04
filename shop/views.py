from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from cart.forms import CartAddProductForm


def product_list(request, category_slug=None):
    products = None
    category = None
    categories = Category.objects.all()
    if category_slug:
        language = request.LANGUAGE_CODE
        category = get_object_or_404(Category, translations__language_code=language, translations__slug=category_slug)
        products = Product.objects.filter(category=category, available=True)
    return render(request, 'shop/product/list.html',
                  {'categories': categories,
                   'products': products,
                   'category': category})


def product_detail(request, slug, id):
    cart_product_form = CartAddProductForm()
    language = request.LANGUAGE_CODE
    product = get_object_or_404(Product, id=id,
                                translations__language_code=language,
                                translations__slug=slug,
                                available=True)
    return render(request, 'shop/product/detail.html', {'product': product, 'cart_product_form': cart_product_form})
