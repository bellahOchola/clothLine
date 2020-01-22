from . import views
from django.urls  import path, include

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('product/<id>', views.product, name='product' ),
    path('cart/<id>', views.add_cart, name='cart'),
    path('order/', views.order_summary, name='order_summary'),
    path('checkout/', views.check_out, name='checkout'),
    path('accounts/', include('allauth.urls')),
]

