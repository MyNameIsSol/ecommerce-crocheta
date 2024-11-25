from django.shortcuts import render,get_object_or_404
from . models import Product, ProductGallery
from category.models import Category
from cart.models import CartItem
from cart.views import _cart_id
import random
from django.db.models import Q
from django.utils.html import escape

# Create your views here.

def store(request, category_slug=None):
    # products = Product.objects.all().filter(is_available = True)
    # product_count = products.count()

    categories = None
    products = None
    category_details = None

    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        category_details = Category.objects.get(slug=category_slug)
        products = Product.objects.filter(category = categories, is_available = True)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available = True)
        product_count = products.count()

    context = {
        'category_detail' : category_details,
        'products' : products,
        'product_count' : product_count,
    }
    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id = _cart_id(request), product = single_product).exists()
    except Exception as e:
        raise e
    
    products = Product.objects.order_by('-created_date').filter(Q(description__icontains=single_product.product_name) | Q(category__slug=category_slug))
    product_gallery = ProductGallery.objects.filter(product_id=single_product.id)
    
    context = {
        'single_product' : single_product,
        'in_cart' : in_cart,
        'product_gallery' : product_gallery,
        'products' : products,
    }
    return render(request, 'store/product_detail.html', context)


def search(request):
    if 'search' in request.GET:
        keyword = request.GET['search']
        keyword = escape(keyword.strip())  # Sanitize and clean keyword

        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count = products.count()
    
    context = {
        'products' : products,
        'product_count' : product_count,
    }
    return render(request, 'store/store.html', context)


