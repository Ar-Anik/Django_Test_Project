from django.shortcuts import render, redirect, get_object_or_404

from .models import Product
from .models import Cart
from .models import Order
from .models import Review
from .models import FAQ
from .forms import ProductForm
from .forms import ReviewForm


from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.

# def showProduct(request) :
#     products = Product.objects.all()

#     user_count = User.objects.count()
#     product_count = Product.objects.count()

#     context = {
#         'products' : products,
#         'u_c' : user_count,
#         'p_c' : product_count
#     }
#     return render(request, 'ProductManagement/products.html', context)

def showProduct(request):
    
    products = Product.objects.all()


    if request.method == 'POST':
        products = Product.objects.filter(name__icontains = request.POST['search'])
        category = Product.objects.filter(category__icontains = request.POST['search'])
        description = Product.objects.filter(description__icontains = request.POST['search'])

        products = products | category | description # C = A U B set operation

    user_count = User.objects.count()
    product_count = Product.objects.count()

    context = {
        'products' : products,
        'u_c' : user_count,
        'p_c' : product_count
    }
    return render(request, 'ProductManagement/products.html', context)


def showDetails(request, product_id):
    
    searched_product = get_object_or_404(Product, id=product_id)

    form = ReviewForm()

    if request.method == "POST":
        form = ReviewForm(request.POST)

        if form.is_valid:
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()

            searched_product.reviews.add(instance)
            searched_product.save()

    context = {
        'search': searched_product,
        'form': form
    }
    return render(request, 'ProductManagement/product_detail.html', context)

@login_required
def uploadProducts(request) :
    form = ProductForm()

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid() :
            form.save()

            return redirect('products_list')

    context = { 
        'form' : form
    }
    return render(request, 'ProductManagement/upload.html', context)

@login_required
def view_cart(request) :
    cart = Cart.objects.get(user=request.user)

    total = 0

    for i in cart.product.all():
        total += i.price
    
    context = {
        'cart' : cart,
        'total' : total
    }
    return render(request, 'ProductManagement/cart.html', context)

@login_required
def update_cart(request, product_id):

    product = get_object_or_404(Product, id=product_id)
    cart = get_object_or_404(Cart, user=request.user)

    cart.product.add(product)
    cart.save()

    return redirect('cart')

@login_required
def delete_from_cart(request, product_id) :
    product = get_object_or_404(Product, id=product_id)
    cart = Cart.objects.get(user=request.user)

    cart.product.remove(product)
    cart.save()

    return redirect('cart')

@login_required
def my_orders(request) :
    orders = Order(user=request.user)

    try:
        orders = Order.objects.filter(user=request.user)
        order_status = True
    except orders.DoesNotExist :
        orders = Order(user=request.user)
        order_status = False
    
    total = 0.0

    for i in orders :
        total += i.product.price

    context = {
        'orders' : orders,
        'order_status' : order_status,
        'total' : total
    }
    return render(request, 'ProductManagement/order.html', context)

@login_required
def make_order(request, product_id) :
    product = get_object_or_404(Product, id = product_id)
    order = Order(user=request.user, product=product)
    order.save()

    cart = Cart.objects.get(user=request.user)
    cart.product.remove(product)
    cart.save()

    return redirect('cart')

def bkash_order(request, product_id) :
    product = get_object_or_404(Product, id=product_id)

    order = Order(user=request.user, product=product)

    order.transaction_id = request.POST['transaction_id']
    order.payment_options = 'Bkash'
    order.save()

    cart = Cart.objects.get(user=request.user)
    cart.product.remove(product)
    cart.save()

    return redirect('cart')

def rocket_order(request, product_id) :
    product = get_object_or_404(Product, id=product_id)

    order = Order(user=request.user, product=product)

    order.transaction_id = request.POST['transaction_id']
    order.payment_options = 'Rocket'
    order.save()

    cart = Cart.objects.get(user=request.user)
    cart.product.remove(product)
    cart.save()

    return redirect('cart')

@login_required
def review_after_complete(request, product_id):

    already_reviewed = False

    searched_product = get_object_or_404(Product, id=product_id)

    user_list = searched_product.reviews.filter(user=request.user)
    print(user_list, len(user_list))
    if len(user_list) != 0:
        already_reviewed = True


    form = ReviewForm()

    if request.method == "POST":
        form = ReviewForm(request.POST)

        if form.is_valid:
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()

            searched_product.reviews.add(instance)
            searched_product.save()

            return redirect('my-orders')

    context = {
        'search': searched_product,
        'form': form,
        'already_reviewed': already_reviewed
    }
    return render(request, 'ProductManagement/review.html', context)

def Faq_details(request):
    faq = FAQ.objects.filter(status=True).order_by('created_at')

    context = {
        'faq' : faq,
    }

    return render(request, 'ProductManagement/faq.html', context)
