from django.db import models
from category.models import Category
from django.urls import reverse

# Create your models here.
class Product(models.Model):
    unit_choices = [('pcs','Pcs'),('pair','Pair'),('doz','Doz'),('box','Box'),('pack','Pack'),('bag','Bag')]
    collection_choices = [('latest','Latest'),('special','Special'),('featured','Featured')]
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(max_length=500, blank=True)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    discount_price = models.DecimalField(max_digits=9, decimal_places=2, blank=True, default=0)
    images = models.ImageField(upload_to='photo/products',)
    stock = models.IntegerField(default=0)
    is_available = models.BooleanField(default=True)
    collection = models.CharField(max_length=100, choices=collection_choices, default='latest')
    category= models.ForeignKey(Category, on_delete=models.CASCADE)
    unit= models.CharField(max_length=100, choices=unit_choices, default='pcs')
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now_add=True)

    def update_stock(self):
        """
        Update product stock to reflect the total stock of its variations.
        """
        total_stock = sum(variation.stock for variation in self.variation_set.all())
        self.stock = total_stock
        self.save()

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])
    
    def __str__(self) -> str:
        return self.product_name
    

class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(variation_category = 'color', is_active = True)
    
    def sizes(self):
        return super(VariationManager, self).filter(variation_category = 'size', is_active = True) 


variation_category_choice = (
    ('color', 'color'),
    ('size', 'size'),
)  

class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100, choices=variation_category_choice)
    variation_value = models.CharField(max_length=100)
    stock = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now = True)

    objects = VariationManager()


    def __str__(self):
        return f"{self.variation_value} ({self.stock} in stock)"


class ProductGallery(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='store/products', max_length=255)

    def __str__(self):
        return self.product.product_name
    
    class Meta:
        verbose_name = 'productgallery'
        verbose_name_plural = 'product gallery'