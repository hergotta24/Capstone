# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserCreationForm, UserChangeForm
from .models import *


class UserAdmin(BaseUserAdmin):
    add_form = UserCreationForm

    model = User
    list_display = ["email", "username", "password", "phone_number"]
    fieldsets = (
        *BaseUserAdmin.fieldsets,
        (
            'Additional Information',
            {
                'fields': (
                    'phone_number',
                ),
            },
        ),
    )


# Register models here
admin.site.register(User, UserAdmin)
admin.site.register(Address)
admin.site.register(Storefront)
admin.site.register(StoreReviews)
admin.site.register(Product)
admin.site.register(Favorite)
admin.site.register(ProductImage)
admin.site.register(ProductReviews)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(InvoiceItem)
admin.site.register(Invoice)
admin.site.register(Order)
admin.site.register(OrderItem)
