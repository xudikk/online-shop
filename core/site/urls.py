from django.urls import path
from .views import index, search, ctg, cart, change_cart


urlpatterns = [
    path("", index, name='home'),
    path("ctg/", ctg, name='ctg'),
    path("srch/", search, name='srch'),
    path("cart/", cart, name='cart'),
    path("add-to-cart/<int:add_id>/", cart, name="cart-add"),
    path("ch/cart/<int:cart_id>/<int:inc>/", change_cart, name='change_cart')


]



