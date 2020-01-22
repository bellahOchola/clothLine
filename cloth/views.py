from django.shortcuts import render,redirect
from .forms import RegistrationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from . models import *
from django.contrib import messages


# Create your views here.

def index(request):
    products = Product.objects.all()

    return render(request, 'index.html', {'products':products} )

def signup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = RegistrationForm()
    return render(request, 'registration/signup.html', {'form':form})

def product(request, id):
    product = Product.objects.get(id=id)

    return render(request, 'products.html', {'product':product})

def add_cart(request, id):
    products = Product.objects.get(id=id)
    ordered_product,created = OrderedProduct.objects.get_or_create(products=products, ordered=False,user=request.user) 
    my_order = Order.objects.filter(user=request.user, ordered=False,)
    if my_order.exists():
        order = my_order[0]
        #check if the product is in the order
        if order.product.filter(products__id=products.id).exists():
            ordered_product.quantity +=1
            ordered_product.save()
            messages.info(request, 'This item quantity was updated')
        else:
            messages.info(request, 'This item was successfully added to your cart')
            order.product.add(ordered_product)

    else:
        order = Order.objects.create(user=request.user)
        order.product.add(ordered_product)
        messages.info(request, 'This item was successfully added to your cart')

    return redirect('product', id=id)

def order_summary(request):
    productss = OrderedProduct.objects.all()
    ord = Order.objects.all()
    return render(request, 'summary.html', {'productss':productss, 'ord':ord} )

def check_out(request):
    return render(request, 'checkout.html')
