from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Account

@receiver(post_migrate)
def create_superuser(sender, **kwargs):
    # Check if a superuser already exists
    if not Account.objects.filter(is_superadmin=True).exists():
        # Create the superuser
        Account.objects.create_superuser(
            email='support@crochetandhooks.com',         # Replace with desired email
            username='admin',                 # Replace with desired username
            password='mynameispeacE1$',         # Replace with desired password
            first_name='Peace',               # Replace with desired first name
            last_name='Okoye'                  # Replace with desired last name
        )
        print("Superuser created!")
