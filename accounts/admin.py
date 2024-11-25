from django.contrib import admin
from .models import Account, UserProfile
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

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



class UserProfileAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        # return format_html('<img src="{}" width="30" style="border-radius:50%;">'.format(object.profile_picture.url))
            if object.profile_picture:
                return format_html('<img src="{}" width="30" style="border-radius:50%;">'.format(object.profile_picture.url))
            else:
                return format_html('<img src="/static/images/default-profile.png" width="30" style="border-radius:50%;">')  # Replace with your default image URL

    thumbnail.short_description = 'Profile Picture'
    list_display = ('thumbnail', 'user', 'city', 'state', 'country')


# Register the account model
admin.site.register(Account, AccountAdmin)
admin.site.register(UserProfile,UserProfileAdmin)
