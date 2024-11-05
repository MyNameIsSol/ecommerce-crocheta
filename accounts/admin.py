from django.contrib import admin
from .models import Account
from django.contrib.auth.admin import UserAdmin

# Register your models here.

# create an AcountAdmin class and register it below to help display the account fileds in the admin site
class AccountAdmin(UserAdmin):
    list_display = ('email', 'username','first_name','last_name','last_login','date_joined','is_active')
    list_display_links = ('email',) # this makes the value of a column appear as a link to its editable page. you can add more columns
    readonly_fields = ('last_login', 'date_joined')
    ordering = ('-date_joined',) #we use this date in descending order

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

# Register the account model
admin.site.register(Account, AccountAdmin)
