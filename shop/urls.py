from django.urls import path
from . import views

app_name = 'shop'
urlpatterns = [
    path('', views.ShopLandingView.as_view(), name='shop_landing'),
    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('products/<slug:category_slug>/', views.ProductListByCategoryView.as_view(), name='product_list_by_category'),
    path('products/<int:id>/<str:slug>', views.ProductDetailView.as_view(), name='product_detail'),
]
