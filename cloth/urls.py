from . import views
from django.urls  import path, include

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('product/<id>', views.product, name='product' ),
    path('cart/<id>', views.add_cart, name='cart'),
    path('order/<id>', views.order_summary, name='order_summary'),
    path('checkout/<id>', views.check_out, name='checkout'),
    path('accounts/', include('allauth.urls')),
    path('all_products/', views.all_products, name='all_products'),
    path('paypal-return/', views.paypal_return),
    path('paypal-cancel/', views.paypal_cancel),
    path('please-return-payment/', include('paypal.standard.ipn.urls')),

]

