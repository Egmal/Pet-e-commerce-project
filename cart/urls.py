from django.urls import path
from . import views

app_name = 'cart'
urlpatterns = [
    path('', views.CartView.as_view(), name='cart_detail'),
    path('add/<int:product_id>', views.CartView.as_view(), name='cart_add'),
    path('remove/<int:product_id>', views.CartDeleteItemView.as_view(), name='cart_remove'),
]
