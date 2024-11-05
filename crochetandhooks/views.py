from django.shortcuts import render
from store.models import Product

def home(request):

    products = Product.objects.all().filter(is_available = True)
    latest_products = products.filter(collection="latest")
    special_products = products.filter(collection="special")
    featured_products = products.filter(collection="featured")
    context = {
        'products' : products,
        'latest_products' : latest_products,
        'special_products' : special_products,
        'featured_products' : featured_products
    }
    return render(request, 'home.html', context)
