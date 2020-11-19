from django.urls import path, include
from . import views

from django.contrib.sitemaps.views import sitemap
from .sitemap import ElementSitemap

sitemaps = {
    'sitemap': ElementSitemap
}

app_name='store'
urlpatterns = [
    path('', views.index, name='index'),
    path('product/pay/paypal/<int:pk>', views.make_pay_paypal, name='make_pay_paypal'),
    path('product/pay/paypal/<int:pk>/<str:code>', views.make_pay_paypal, name='make_pay_paypal'),
    path('product/paypal/success/<int:pk>', views.paypal_success, name='paypal_success'),
    path('product/paypal/success/<int:pk>/<str:code>', views.paypal_success, name='paypal_success'),
    path('product/paypal/cancel', views.paypal_cancel, name='paypal_cancel'),

    path('bought', views.bought, name='bought'),

    path('product/payed/detail/<int:pk>', views.detail_pay, name='detail_pay'),
    
    path('product/<int:pk>',views.DetailView.as_view(), name='detail'),
    #path('product/<slug:url_clean>',views.DetailView.as_view(), name='detail'),
    path('product/coupon_apply',views.coupon_apply, name='coupon_apply'),
    path('product/<slug:url_clean>',views.detail, name='detail'),
    path('product/<slug:url_clean>/<str:code>',views.detail, name='detail'),

    #carrito
    path('cart_detail', views.cart_detail, name='cart_detail'),
    path('cart_size', views.cart_size, name='cart_size'),
    path('cart_remove/<int:pk>', views.cart_remove, name='cart_remove'),
    path('add_to_cart/<int:pk>', views.add_to_cart, name='add_to_cart'),
    
    #path('product/<int:pk>/<slug:url_clean>',views.DetailView.as_view(), name='detail'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]
