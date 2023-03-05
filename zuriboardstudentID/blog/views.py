from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
import calendar
import json
from calendar import HTMLCalendar
from datetime import datetime
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .forms import ProductForm
from .models import Customer, Product, Order, OrderItem, ShippingAddress, LikeProduct, Category

# Create your views here.
# login
def signin(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/index')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('login')

    else:
        return render(request, 'login.html')

# logout
@login_required(login_url='login_user')
def logout(request):
    auth.logout(request)
    return redirect('/')

# singup
def signup(request):

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                #log user in and redirect to settings page
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                #create a Profile object for the new user
                user_model = User.objects.get(username=username)
                new_profile = Customer.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('settings')
        else:
            messages.info(request, 'Password Not Matching')
            return redirect('register')
        
    else:
        return render(request, 'register.html')

# home page
@login_required(login_url='login_user')
def index(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
    
    month = month.title()
    month_number = list(calendar.month_name).index(month)
    month_number = int(month_number)

    # get current year
    now = datetime.now()
    current_year = now.year

    p = Paginator(Product.objects.all().order_by('-created_at'), 6)
    page = request.GET.get('page')
    products = p.get_page(page)
    nums = "a" * products.paginator.num_pages

    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    items = order.orderitem_set.all()
    cartItems = order.get_cart_items
    categorys = Category.objects.all()

    user_object = User.objects.get(username=request.user.username)
    user_profile = Customer.objects.get(user=user_object)
    #categorys = Category.objects.all()
    product_list = Product.objects.all().order_by('-created_at')

    context = {'cartItems': cartItems, 'user_profile': user_profile, 'product_list': product_list, 
               'products': products, 'nums': nums, "current_year": current_year, 'categorys': categorys,
              }

    return render(request, 'index.html', context)

def addToCart(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

    #context = {}
    #return render(request, 'index.html', context)
# cart
@login_required(login_url='login_user')
def cart(request):
    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    items = order.orderitem_set.all()
    cartItems = order.get_cart_items

    user_object = User.objects.get(username=request.user.username)
    user_profile = Customer.objects.get(user=user_object)

    context = {'items': items, 'order': order, 'cartItems': cartItems, 'user_profile': user_profile,}
    return render(request, 'cart.html', context)

# delete item
@login_required(login_url='login_user')
def delete_cart(request, order_id):
    order = OrderItem.objects.get(pk=order_id)
    order.delete()

    return redirect('cart')

# Delete all items
@login_required(login_url='login_user')
def delete_cart(request, order_id):
    order = Order.objects.get(pk=order_id)
    order_items = OrderItem.objects.filter(order=order)
    order_items.delete()

    return redirect('cart')

# checkout
def checkout(request):
    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    items = order.orderitem_set.all()
    cartItems = order.get_cart_items

    user_object = User.objects.get(username=request.user.username)
    user_profile = Customer.objects.get(user=user_object)

    context = {'items': items, 'order': order, 'cartItems': cartItems, 'user_profile': user_profile,}
    return render(request, 'checkout.html', context)

# profile page
@login_required(login_url='login_user')
def profile(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Customer.objects.get(user=user_object)
    #user_posts = Post.objects.filter(user=pk)
    #user_post_length = len(user_posts)

    context = {
        'user_object': user_object,
        'user_profile': user_profile,
    }
    return render(request, 'profile.html', context)

# settings
@login_required(login_url='login_user')
def settings(request):
    user_profile = Customer.objects.get(user=request.user)

    if request.method == 'POST':
        
        if request.FILES.get('image') == None:
            image = user_profile.profileimg
            email = request.POST['email']
            location = request.POST['location']

            user_profile.profileimg = image
            user_profile.email = email
            user_profile.location = location
            user_profile.save()
        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            email = request.POST['email']
            location = request.POST['location']

            user_profile.profileimg = image
            user_profile.email = email
            user_profile.location = location
            user_profile.save()
        
        return redirect('settings')
    return render(request, 'settings.html', {'user_profile': user_profile})

#process order
@login_required(login_url='login_user')
def processOrder(request):
    transaction_id = datetime.now().timestamp()
    data = json.loads(request.body)

    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zip'],
        )
    
    return JsonResponse('Payment complete', safe=False)

# show individual product
@login_required(login_url='login_user')
def show_product(request, product_id):
    product = Product.objects.get(pk=product_id)

    return render(request, 'productdetails.html', {'product': product})

# like product
@login_required(login_url='login_user')
def like_product(request):
    username = request.user.username
    product_id = request.GET.get('product_id')

    product = Product.objects.get(id=product_id)

    like_filter = LikeProduct.objects.filter(product_id=product_id, username=username).first()

    if like_filter == None:
        new_like = LikeProduct.objects.create(product_id=product_id, username=username)
        new_like.save()
        product.no_of_likes = product.no_of_likes+1
        product.save()
        return redirect('index')
    else:
        like_filter.delete()
        product.no_of_likes = product.no_of_likes-1
        product.save()
        return redirect('index')

# search product
def search_product(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        products = Product.objects.filter(name__contains=searched)

        return render(request, 'search.html', {'searched': searched, 'products': products})
    else:
        return render(request, 'search.html', {})    
# show category
def show_category(request, category_id):
    #user_profile = Profile.objects.get(user=request.user)
    category = Category.objects.get(pk=category_id)
    category_products = Product.objects.filter(category__in=[category])

    p = Paginator(Product.objects.filter(category__in=[category]), 2)
    page = request.GET.get('page')
    products = p.get_page(page)
    nums = "a" * products.paginator.num_pages

    user_object = User.objects.get(username=request.user.username)
    user_profile = Customer.objects.get(user=user_object)

    context = {
        'category_products': category_products, 'user_profile': user_profile,
        'category': category, 'products': products, 'nums': nums,
    }
    return render(request, 'about.html', context)