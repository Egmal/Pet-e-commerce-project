from parler.views import TranslatableSlugMixin
from django.shortcuts import get_object_or_404, render
from .models import Category, Product
from cart.forms import CartAddProductForm
from django.views.generic import DetailView, ListView, View


class ShopLanding(View):
    def get(self, request):
        last_products = Product.objects.all()[:4]
        return render(request, 'shop/landing.html', {'last_products': last_products})


class ProductList(ListView):
    model = Product
    paginate_by = 10
    template_name = 'shop/product/product_list.html'
    context_object_name = 'products'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        context['categories'] = Category.objects.all()
        return context


class ProductListByCategory(ListView):
    model = Product
    paginate_by = 10
    template_name = 'shop/product/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        language = self.request.LANGUAGE_CODE
        category_slug = self.kwargs['category_slug']
        self.category = get_object_or_404(Category, translations__language_code=language,
                                          translations__slug=category_slug)
        queryset = Product.objects.filter(
            category=self.category, available=True)
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        context['category'] = self.category
        context['categories'] = Category.objects.all()
        return context


class ProductDetail(TranslatableSlugMixin, DetailView):
    model = Product
    template_name = 'shop/product/product_detail.html'
    cart_product_form = CartAddProductForm()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart_product_form'] = self.cart_product_form
        return context
