from django import views
from django.urls import path
from .views import *
from order.views import add_to_shoppingcart, remove_from_cart, remove_single_item_from_cart
from django.conf import settings
from django.conf.urls.static import static
from .views import registerPage, loginPage, logoutUser

urlpatterns = [
    path('', Home.as_view(), name='index'),
    path('cart.html', OrderSummaryView.as_view(), name='order-summary'),
    path('shop.html', ShopView.as_view(), name='shop'),
    path('product.html/<slug>/', ProductDetailView.as_view(), name='product'),
    path('add-to-shoppingcart/<slug>/', add_to_shoppingcart, name='add-to-shoppingcart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-single-item-from-cart/<slug>/', remove_single_item_from_cart, name='remove-single-item-from-cart'),
    path('register/',registerPage, name='register'),
    path('login/',loginPage, name='login'),
    path('logout/',logoutUser, name='logout'),
    path('search',searchView, name='search')
]   
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)