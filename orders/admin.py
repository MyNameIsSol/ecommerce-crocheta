from django.contrib import admin
from .models import Payment, ShippingMethod, Order, OrderProduct
# Register your models here.

#we will add the OrderProducts table below the Order table(This will enable us see all the product associated to a particular order) by creating a OrderProductInline class and assinging the OrderProduct class to a model variable. 
class OrderProductInline(admin.TabularInline):
    model = OrderProduct 
    readonly_fields = ('payment', 'user', 'product', 'quantity', 'product_price', 'ordered') # This will make the fields not to be editable because they are important for the user
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'full_name', 'phone', 'email', 'city', 'order_total', 'tax', 'status', 'is_ordered', 'created_at']
    list_filter = ['status', 'is_ordered']
    search_fields = ['order_number', 'first_name', 'last_name', 'phone', 'email']
    list_per_page = 20
    inlines = [OrderProductInline]

admin.site.register(Payment)
admin.site.register(ShippingMethod)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderProduct)
