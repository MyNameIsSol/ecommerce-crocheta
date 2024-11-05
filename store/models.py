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
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    collection = models.CharField(max_length=100, choices=collection_choices, default='latest')
    category= models.ForeignKey(Category, on_delete=models.CASCADE)
    unit= models.CharField(max_length=100, choices=unit_choices, default='pcs')
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now_add=True)

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])
