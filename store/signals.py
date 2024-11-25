from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Variation, Product

@receiver(post_save, sender=Variation)
@receiver(post_delete, sender=Variation)
def update_product_stock(sender, instance, **kwargs):
    """
    Update the total stock of the product whenever a variation is saved or deleted.
    """
    product = instance.product  # Get the product associated with the variation
    if product:  # Ensure the product exists
        product.update_stock()
