"""
URL configuration for Crap project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from BackendWork.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('login/', UserLoginView.as_view(), name='UserLoginView'),
                  path('register/', UserRegisterView.as_view(), name='UserRegisterView'),
                  path('logout/', custom_logout, name='Logout'),
                  path('account/', AccountManagementView.as_view(), name='AccountManagementView'),
                  path('storefront/', StorefrontView.as_view(), name='StorefrontView'),
                  path('updateCartQty/', updateCartQty, name='updateCartQty'),
                  path('orderhistory/', OrderHistoryView.as_view(), name='OrderHistoryView'),
                  path('favorite/', SavedProductView.as_view(), name='SavedProductView'),
                  path('storefront/<int:product_id>/', UpdateProductView.as_view(), name='EditProductView'),
                  path('createproduct/', createproduct, name='createproduct'),
                  path('addFavorite/', addFavorite, name='addFavorite'),
                  path('removeFavorite/', removeFavorite, name='removeFavorite'),
                  path('products/<int:product_id>/', ProductDetailView.as_view(), name='product_detail'),
                  path('review-product/<int:product_id>/', ReviewProductView.as_view(), name='review_product'),
                  path('shop/<int:store_id>/', VendorView.as_view(), name='vendor'),
                  path('addproduct/<int:store_id>/', AddProductView.as_view(), name='AddProductView'),
                  path('delete/<int:productid>/', deleteProduct, name='deleteProduct'),
                  path('', home, name='home'),
                  path('filter/<str:category>/', categoryFilter, name='categoryFilter'),
                  path('search/', search, name='search'),
                  path('cart/', AccountCartView.as_view(), name='AccountCartView'),
                  path('checkout/', checkout_view, name='checkout'),
                  path('paypal/', include('paypal.standard.ipn.urls')),
                  path('payment-completed/<int:invoice_id>/', payment_complete_view, name='payment-complete'),
                  path('payment-failed/<int:invoice_id>', payment_failed_view, name='payment-failed'),
                  # path('download/invoice/<int:invoice_id>', generate_invoice, name='download_invoice'),
                  path('add-shipping-details/', add_shipping_details, name='add_shipping_details'),
                  path('remove-from-cart/<int:product_id>/', removeFromCart, name='removeFromCart')
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
