from parler.views import TranslatableSlugMixin
from django.shortcuts import get_object_or_404, render
from .models import Category, Product
from cart.forms import CartAddProductForm
from django.views.generic import DetailView, View, ListView


class ShopLandingView(View):
    def get(self, request):
        categories  =  Category.objects.translated(request.LANGUAGE_CODE).all()
        return render(request, 'shop/landing.html', {'categories': categories})


class ProductListView(ListView):
    model = Product
    paginate_by = 5
    template_name = 'shop/product/product_list.html'
    context_object_name = 'products'
    category = None
    language = None 

    def get_queryset(self, category=None):     
        self.language = self.request.LANGUAGE_CODE
        if category is None:
            queryset = Product.objects.translated(self.language).filter(available=True)
        else:
            category_slug = self.kwargs['category_slug']
            self.category = get_object_or_404(Category, translations__language_code=self.language,
                                          translations__slug=category_slug)
            queryset = Product.objects.translated(self.language).filter(category=self.category, available=True)
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        context['category'] = self.category
        context['categories'] = Category.objects.translated(self.language).all()
        return context


class ProductDetailView(TranslatableSlugMixin, DetailView):
    model = Product
    template_name = 'shop/product/product_detail.html'
    cart_product_form = CartAddProductForm()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart_product_form'] = self.cart_product_form
        return context
    