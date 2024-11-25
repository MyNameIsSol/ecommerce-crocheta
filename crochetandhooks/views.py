from django.shortcuts import render, redirect
from store.models import Product
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings

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


def about(request):
    return render(request, 'about.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        if name and email and message:
            # Compose the message
            subject = f"New Contact Message from {name}"
            admin_message = f"Message from {name} ({email}):\n\n{message}"

            # Send email to admin
            try:
                send_mail(
                    subject,
                    admin_message,
                    settings.DEFAULT_FROM_EMAIL,  # Ensure this is set in your settings.py
                    [settings.ADMINS_EMAIL],  # Replace with admin's email
                )
                messages.success(request, "Your message has been sent successfully!")
                return redirect('contact')  # Replace 'contact' with your desired redirect URL
            except Exception as e:
                messages.error(request, f"Failed to send your message. Error: {str(e)}")
        else:
            messages.error(request, "All fields are required!")
    
    return render(request, 'contact.html')


def service(request):
    return render(request, 'service.html')

def terms(request):
    return render(request, 'terms.html')
