from django.shortcuts import render,redirect
from .forms import RegistrationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from . models import *
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm


# Create your views here.

def index(request):
    products = Product.objects.all()
    return render(request, 'index.html', {'products':products} )


def all_products(request):
    products = Product.objects.all()
    return render (request, 'all_products.html', {'products':products})

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

def order_summary(request, id):
    productss = OrderedProduct.objects.filter(user = id)
    ord = Order.objects.filter(user = id)
    # product = Product.objects.get(id=id)
    # productss = OrderedProduct.objects.filter(products=product)
    # ord = Order.objects.all()
    return render(request, 'summary.html', {'productss':productss, 'ord':ord})

def check_out(request, id):
    ord = Order.objects.filter(user = id)

    args ={}
    paypal_dict = {
        'business' : 'bellahkenya@gmail.com',
        'amount': '20.00',
        'currency_code': 'USD',
        'item_name': 'clothings',
        'invoice':  'unique-invoice-001',
        'notify_url': 'http://127.0.0.1:8000/please-return-payment/',
        'return_url': 'http://127.0.0.1:8000/paypal-return/',
        'cancel_return': 'http://127.0.0.1:8000/paypal-cancel/'
    }

    form = PayPalPaymentsForm(initial=paypal_dict)

    return render(request, 'checkout.html', {'ord':ord,'form':form})

@csrf_exempt
def paypal_return(request):
    args = {
        'post': request.POST,
        'get': request.GET
    }
    return render(request, 'paypal_return.html', args)

def paypal_cancel(request):
    args = {
        'post': request.POST,
        'get': request.GET
    }
    return render(request, 'paypal_cancel.html', args)