from django.urls import path
from .views import get_products, post_products, update_product, update_cart, get_cart, order

urlpatterns = [
    path("products", get_products, name='get_products'),
    path("product/", post_products, name='create_product'),
    path("product/<int:pk>", update_product, name='change_product'),

    path("cart", get_cart, name='get_carts'),
    path("cart/<int:pk>", update_cart, name='change_cart'),

    path("order", order, name='get_or_make_order')
]