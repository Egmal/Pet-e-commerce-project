from django.urls import path
from . import views

app_name = 'shop'
urlpatterns = [
    path('', views.ShopLanding.as_view(), name='shop_landing'),
    path('products/', views.ProductList.as_view(), name='product_list'),
    path('products/<slug:category_slug>/', views.ProductListByCategory.as_view(), name='product_list_by_category'),
    path('products/<int:id>/<str:slug>', views.ProductDetail.as_view(), name='product_detail'),
]
