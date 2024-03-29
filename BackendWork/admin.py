# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import UserCreationForm, UserChangeForm
from .models import (User, Address, Storefront, StoreReviews, Product, ProductImage, ProductReviews, Invoice, LineItem)


class UserAdmin(UserAdmin):
    add_form = UserCreationForm

    model = User
    list_display = ["email", "username", "password", "phone_number", "shipping_address", "billing_address"]
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Additional Information',
            {
                'fields': (
                    'phone_number',
                    'shipping_address',
                    'billing_address',
                    'favorite',
                )
            }
        )
    )


# Register models here
admin.site.register(User, UserAdmin)
admin.site.register(Address)
admin.site.register(Storefront)
admin.site.register(StoreReviews)
admin.site.register(Product)
# admin.site.register(Category)
# admin.site.register(SubCategory)
admin.site.register(ProductImage)
admin.site.register(ProductReviews)
admin.site.register(Invoice)
admin.site.register(LineItem)
