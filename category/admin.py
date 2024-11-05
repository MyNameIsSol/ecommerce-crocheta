from django.contrib import admin
from .models import Category

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug':('category_name',)
    }
    list_display = ('category_name', 'slug')

# register the Category and CategoryAdmin model   
admin.site.register(Category, CategoryAdmin)
