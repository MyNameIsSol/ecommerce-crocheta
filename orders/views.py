from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from cart.models import CartItem
from .forms import OrderForm
import datetime
from .models import ShippingMethod, Order, Payment, OrderProduct
import json
from store.models import Product
from django.template.loader import render_to_string 
from django.core.mail import EmailMessage 

# for handling proof file
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os

# Create your views here.
def payments(request):
    if request.method == "POST":
        shippingID = request.POST.get('shippingID')
        orderID = request.POST.get('orderID')
        transID = request.POST.get('transID')
        payment_method = request.POST.get('payment_method')
        status = request.POST.get('status')
        transRef = request.POST.get('transRef')
        # Handle the uploaded file
        file_path = ""
        proof_file = request.FILES.get('proof')
        if proof_file:
            # Save the file (e.g., to MEDIA_ROOT)
            file_path = default_storage.save(f"paymentproof/{proof_file.name}", ContentFile(proof_file.read()))
        # We will get the user order
        order = Order.objects.get(user=request.user, is_ordered=False, order_number=orderID)
        # shipping_method = ShippingMethod.objects.get(id=shippingID)
        payment = Payment(
            user=request.user,
            payment_id=transID,
            payment_ref=transRef,
            payment_proof=file_path,
            payment_method=payment_method,
            amount_paid=order.order_total,
            status=status,
        )
        payment.save()
        order.payment = payment
        order.is_ordered = True
        order.save()
        # We will store the user cartitems in the OrderProduct table
        cart_items = CartItem.objects.filter(user=request.user)
        for item in cart_items:
            orderproduct = OrderProduct()
            orderproduct.order_id = order.id
            orderproduct.shipping_method_id = shippingID
            orderproduct.payment = payment
            orderproduct.user_id = request.user.id
            orderproduct.product_id = item.product_id
            orderproduct.quantity = item.quantity
            orderproduct.product_price = item.product.price
            orderproduct.ordered = True
            orderproduct.save()
            # We will save the product variation
            cart_item = CartItem.objects.get(id=item.id)
            product_variation = cart_item.variations.all()
            orderproduct = OrderProduct.objects.get(id=orderproduct.id)
            orderproduct.variations.set(product_variation)
            orderproduct.save()
            #We will reduce the product number
            # product = Product.objects.get(id=item.product_id)
            # product.stock -= item.quantity
            # product.save()
            # Reduce stock for each variation(NEW)
            for variation in product_variation:
                variation.stock -= item.quantity
                variation.save()
        # Delete user cart after payment
        CartItem.objects.filter(user=request.user).delete()
        # Send order received email to user
        mail_subject = 'Thank you for your order!'
        message = render_to_string('orders/order_received_email.html', {
            'user': request.user,
            'order': order,
            'payment':payment,
        })
        to_email = request.user.email
        send_email = EmailMessage(mail_subject, message, to=[to_email])
        send_email.content_subtype = "html"
        send_email.encoding = "utf-8"
        send_email.send()
        data = {
            'order_number' : order.order_number,
            'transID' : payment.payment_id,
            'transRef' : payment.payment_ref,
        }
        return JsonResponse(data) # This (data) will go to the place were it came, which is the js function in the payments.html file
        # return render(request, 'orders/payments.html')
    else:
        return redirect('cart')


def place_order(request, total=0, quantity=0):
    
    current_user = request.user
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')
    
    
    if request.method == "POST":
        shipping_id = request.POST['shipping_method']
        shipping_method = ShippingMethod.objects.get(id=shipping_id)
        # print(shipping_method)
        # We will calculate the grand_total
        grand_total = 0
        tax = 0
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (0 * total)/100
        grand_total = total + tax + shipping_method.price # ends

        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order()
            data.user = current_user
            data.shipping_method = shipping_method
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.postcode = form.cleaned_data['postcode']
            data.order_note = form.cleaned_data['order_note']

            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()

            # Creating order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d")

            order_number = current_date + str(data.id) # order number created
            data.order_number = order_number
            data.save() # Save the order

            # Send the order to the payment.html page
            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
            context = {
                'order':order,
                'cart_items': cart_items,
                'total':total,
                'shipping_fee': shipping_method.price,
                'shipping_id': shipping_id,
                'tax':tax,
                'grand_total': grand_total,
            }
            return render(request, 'orders/payments.html', context)
            # return redirect('checkout')
        else:
            messages.error(request, f"Form errors: {form.errors}")
            return redirect('checkout')
    else:
        return redirect('checkout')


def order_complete(request):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')
    transRef = request.GET.get('payment_ref')
    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_products = OrderProduct.objects.filter(order_id=order.id)
        payment = Payment.objects.get(payment_id=transID)

        #Calculate for subtotal
        subtotal = 0
        for i in ordered_products:
            subtotal += i.product_price * i.quantity

        context = {
            'order' : order,
            'ordered_products' : ordered_products,
            'payment':payment,
            'order_number': order.order_number,
            'transID': payment.payment_id,
            'subtotal': subtotal,
        }

        return render(request, 'orders/order_complete.html', context)
    except(Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('home')