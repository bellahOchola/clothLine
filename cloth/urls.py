from . import views
from django.urls  import path, include

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('account/', include('django.contrib.auth.urls')),
    path('product/<id>', views.product, name='product' ),
    path('cart/<id>', views.add_cart, name='cart'),
]

