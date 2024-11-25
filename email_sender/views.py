from django.urls import reverse
from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from accounts.models import Account


# Create your views here.

def send_email_view(request):
    if request.method == 'POST':
        subject = request.POST.get("subject")
        message = request.POST.get("message")
        current_site = get_current_site(request)
        print(message)
        if subject and message:
        # Get all active users
            users = Account.objects.all()  # Or any custom user model
            for user in users:
                if user.email:
                    # Create the email content
                    email_content = render_to_string('email_sender/send_email_message.html', {
                        'user': user,
                        'message': message,
                        'domain': current_site,
                    })
                    email = EmailMessage(subject, email_content, to=[user.email])
                    email.content_subtype = "html"
                    email.encoding = "utf-8"
                    email.send()
                    print("Sent!")
                    # Save the email log (optional)
                    # EmailLog.objects.create(subject=subject, recipient=user.email, message=message)

            messages.success(request, "Emails sent successfully!")
            return redirect(reverse('admin:email_sender_emaillog_changelist'))  # Redirect to admin EmailLog
            # return redirect('send-email')  # Redirect to an appropriate page
        else:
            messages.error(request, "Both subject and message are required!")

    return render(request, 'email_sender/send_email_form.html')
