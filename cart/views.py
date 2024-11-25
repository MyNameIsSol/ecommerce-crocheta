from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from store.models import Product, Variation
from .models import Cart, CartItem
from orders.models import ShippingMethod
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

# Create your views here.

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id)

    if current_user.is_authenticated: #IF USER IS LOGGEDIN USE THIS CODE

        product_variation = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]
                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                except Variation.DoesNotExist:
                    # If the variation is not found, skip it
                    continue

        # Handle cases where no variation is selected
        if len(product_variation) == 0:
            messages.error(request, "Please select a variation (e.g., size or color) before adding the product to your cart.")
            return redirect(product.get_url())  # Redirect back to product_detail

        # Check stock for the selected variation(NEW)
        if any(variation.stock <= 0 for variation in product_variation):
            messages.error(request, "The selected variation is out of stock.")
            return redirect(product.get_url())
        
        # try:
        #     cart = Cart.objects.get(cart_id=_cart_id(request))
        # except Cart.DoesNotExist:
        #     cart = Cart.objects.create(
        #         cart_id = _cart_id(request))
        # cart.save()

        # try:
        cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists()
        if cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, user=current_user)

            ex_var_list = []
            id = []
            for item in cart_item: 
                existing_variation = item.variations.all() # get all existing variation of the cart item in the CartItem table
                ex_var_list.append(list(existing_variation)) # put the existing variations found in a list
                id.append(item.id)

            if(product_variation in ex_var_list): # Check if the same posted cart item has same variation already in the CartItem table
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)

                total_quantity = item.quantity + 1 #(NEW)
                if total_quantity > min(variation.stock for variation in product_variation):
                    messages.error(request, "The requested quantity exceeds available stock.")
                    return redirect('cart')

                item.quantity += 1 # if the cart item has same variation in the CartItem table, just add the quantity
                item.save()
            else:
                item  = CartItem.objects.create(product=product, quantity=1, user=current_user)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)

                item.save()
        # except CartItem.DoesNotExist:
        else:
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                user = current_user,
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)

            cart_item.save()
        return redirect('cart')

    else:  # IF USER IS NOT LOGGED IN, USE THIS CODE
        product_variation = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]
                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                except Variation.DoesNotExist:
                    # If the variation is not found, skip it
                    continue

        # Handle cases where no variation is selected
        if len(product_variation) == 0:
            messages.error(request, "Please select a variation (e.g., size or color) before adding the product to your cart.")
            return redirect(product.get_url())  # Redirect back to product_detail

        # Check stock for the selected variation(NEW)
        if any(variation.stock <= 0 for variation in product_variation):
            messages.error(request, "One or more selected variations are out of stock.")
            return redirect(product.get_url())

        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id = _cart_id(request))
        cart.save()

        # try:
        cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
        if cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, cart=cart)

            ex_var_list = []
            id = []
            for item in cart_item: 
                existing_variation = item.variations.all() # get all existing variation of the cart item in the CartItem table
                ex_var_list.append(list(existing_variation)) # put the existing variations found in a list
                id.append(item.id)

            if(product_variation in ex_var_list): # Check if the same posted cart item has same variation already in the CartItem table
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)

                total_quantity = item.quantity + 1 #(NEW)
                if total_quantity > min(variation.stock for variation in product_variation):
                    messages.error(request, "The requested quantity exceeds available stock.")
                    return redirect('cart')

                item.quantity += 1 # if the cart item has same variation in the CartItem table, just add the quantity
                item.save()
            else:
                item  = CartItem.objects.create(product=product, quantity=1, cart=cart)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)

                item.save()
        # except CartItem.DoesNotExist:
        else:
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                cart = cart,
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)

            cart_item.save()
        return redirect('cart')


def remove_cart(request, product_id, cart_item_id):
    # cart = Cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    # cart_item = CartItem.objects.get(product = product, cart = cart, id=cart_item_id)

    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product = product, user = request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id = _cart_id(request))
            cart_item = CartItem.objects.get(product = product, cart = cart, id=cart_item_id)  
        
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass

    return redirect('cart')


def remove_cart_item(request, product_id, cart_item_id):
    # cart = Cart.objects.get(cart_id = _cart_id(request))  
    product = get_object_or_404(Product, id=product_id)

    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product = product, user = request.user, id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id = _cart_id(request))
        cart_item = CartItem.objects.get(product = product, cart = cart, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')
    


def cart(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0

        if request.user.is_authenticated: 
            cart_items = CartItem.objects.filter(user=request.user, is_active = True)
            cart_items_count = cart_items.count()
        else:
            cart = Cart.objects.get(cart_id = _cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
            cart_items_count = cart_items.count()

        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        
        tax = (0 * total) / 100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass

    context = {
        'total' : total,
        'quantity' : quantity,
        'cart_items' : cart_items,
        'tax' : tax,
        'grand_total' : grand_total,
        'cart_items_count' : cart_items_count
    }
    return render(request, 'store/cart.html', context)

@login_required(login_url='login')
def checkout(request, total=0, quantity=0, cart_items = None):
    try: 
        shipping_methods = ShippingMethod.objects.all()
        print(shipping_methods)
        tax = 0
        grand_total = 0
        if request.user.is_authenticated: # 261b
            cart_items = CartItem.objects.filter(user=request.user, is_active = True)
        else:
            cart = Cart.objects.get(cart_id = _cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active = True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (0 * total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass
    context = {
        'total' : total,
        'quantity' : quantity,
        'cart_items' : cart_items, 
        # 227h we will send the tax and the grand_total to the checkout.html file
        'tax' : tax,
        'grand_total' : grand_total,
        'shipping_methods' : shipping_methods
    }
    return render(request, 'store/checkout.html', context)