# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from BackendWork.models import *

from .forms import UserCreationForm
from .models import (User, Address, Storefront, StoreReviews, Product, ProductImage, ProductReviews,
                     Cart, CartItem)


class UserAdmin(UserAdmin):
    add_form = UserCreationForm

    model = User
    list_display = ["email", "username", "password", "phone_number"]
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Additional Information',
            {
                'fields': (
                    'phone_number',
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
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(InvoiceItem)
admin.site.register(Invoice)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ProductImage)
admin.site.register(ProductReviews)
