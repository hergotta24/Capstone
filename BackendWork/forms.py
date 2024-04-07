# accounts/forms.py
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import User, Product, Storefront, ProductImage
from paypal.standard.forms import PayPalPaymentsForm
from django.utils.html import format_html


class CustomPayPalPaymentsForm(PayPalPaymentsForm):
    def render(self):
        form_open = f'<form class="w-75" action="{self.get_login_url()}" method="post">'
        hidden_fields = ''.join([
            f'<input type="hidden" name="{field.name}" value="{field.value()}" id="{field.auto_id}">'
            for field in self
        ])
        submit_button = '<input type="submit" name="submit" alt="Buy it Now" value="Buy Now" class="bg-success my-2 primary-color py-2 rounded w-100">'
        form_close = '</form>'
        return format_html(f"{form_open}{hidden_fields}{submit_button}{form_close}")


class UserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "username", "first_name", "last_name", "phone_number")

    def clean_confirm_password(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password1')
        confirm_password = cleaned_data.get('password2')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords don't match")
        return confirm_password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


#
# class CardCreationForm(forms.ModelForm):
#     class Meta:
#         model = Payment
#         fields = ("name", "card_number", "expiration_date", "back_number")
#
#
# class LineItemCreationForm(forms.ModelForm):
#     class Meta:
#         model = LineItem
#         fields = ("invoiceId", "productId", "quantity", "linePrice")


class StorefrontForm(forms.ModelForm):
    class Meta:
        model = Storefront
        fields = ['name', 'description', 'bannerImage', 'logoImage']


class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['soldByStoreId', 'name', 'description', 'price', 'qoh', 'category', 'weight',
                  'length', 'width', 'height']


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image']
