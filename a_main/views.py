from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
import time
import datetime
from .models import *
from .forms import *


def homepage(request, tag=None):
    if tag:
        products = Product.objects.filter(tags__slug=tag)
        tag = get_object_or_404(Tag, slug=tag)
    else:
        products = Product.objects.all()
    categories = Tag.objects.all()
   
    user = request.user
    if user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_items':0, 'get_cart_total':0, 'vat':0, 'get_order_total':0} 
        cartItems = order['get_cart_items']
        
    context  = {
        'items': items,
        'order': order,
        'cartItems':cartItems,
        'products': products,
        'tag': tag,
        'categories': categories,
        }  
    return render(request, 'a_main/home.html', context)


def shop(request):
    categories=Tag.objects.all()
    products = Product.objects.all()
    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'a_main/shop-grid.html', context)


def product_details(request, pk):
    product = get_object_or_404(Product, id=pk)
    related_products = Product.objects.filter(tags__in=product.tags.all()).exclude(id=pk)[:8]
    reviews = product.review_set.all()
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        item = order.orderitem_set.filter(product=product).first()
        if item:
            item_quantity = item.quantity
        else:
            item_quantity = 0
       
        cartItems = order.get_cart_items
    else:
        item = []
        order = {'get_cart_items':0, 'get_cart_total':0, 'vat':0, 'get_order_total':0} 
        cartItems = order['get_cart_items']
    context = {
        'product': product,
        'related_products': related_products,
        'cartItems': cartItems,
        'item':item,
        'item_quantity': item_quantity,
        'reviews':reviews,
    }    
    return render(request, 'a_main/product-details.html',context)



def blog(request):
    return render(request, 'a_main/blog.html')

def blog_details(request):
    return render(request, 'a_main/blog-details.html')

def contact(request):
    return render(request, 'a_main/contact.html')



@login_required
def create_product(request):
    form = CreateProductForm()
    if request.method == 'POST':
        form = CreateProductForm(request.POST, request.FILES)
        if form.is_valid():
            new_product =form.save(commit=False)
            new_product.seller = request.user
            new_product.save()
            form.save_m2m()
            messages.success(request, "Product created successfully')")
            return redirect('homepage')
    return render(request, 'a_main/post_product.html', {'form': form})

def shopping_cart(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_items':0, 'get_cart_total':0, 'vat':0, 'get_order_total':0}
        cartItems = order['get_cart_items']
    context  = {
        'items': items,
        'order': order,
        'cartItems': cartItems,
    }
    return render(request, 'a_main/shopping-cart.html', context)

@login_required
def checkout(request):
    user = request.user
    if user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_items':0, 'get_cart_total':0, 'vat':0, 'get_order_total':0}
        cartItems = order['get_cart_items'] 
        
    context  = {
        'items': items,
        'order': order,
        'cartItems': cartItems,
        }  
    return render(request, 'a_main/checkout.html', context)

def update_item(request):
    data = json.loads(request.body)
    productId = data.get('productId')
    action = data.get('action')
    
    print('ProductId:', productId)
    print('Action:', action)
    
    customer=request.user.customer
    product= Product.objects.get(id=productId) 
    order, created = Order.objects.get_or_create(customer=customer,complete = False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
        messages.success(request,'Cart Updated!')
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
        messages.success(request,'Item removed successfully!')
    orderItem.save()
    
    if orderItem.quantity <= 0:
        orderItem.delete()
        messages.success(request,'Item deleted successfully!')
   
    return JsonResponse('Item was added successfully', safe=False)



def processOrder(request):
    unique_info = 'ORDER'
    transaction_id = f"{unique_info}-{str(datetime.datetime.now())}"
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total']) 
        order.order_id = transaction_id
        
        if total == float(order.get_order_total):
            if total > 0:
                order.complete = True
                order.save()
                messages.success(request,'Your Order has been Confirmed!')
            else:
                return redirect('orders')
       
    else:
        print("User is not authenticated")
    return JsonResponse('Your Order has been confirmed successfully', safe=False)