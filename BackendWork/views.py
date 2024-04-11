from _ast import Store

from django.contrib.auth import authenticate, login, logout
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.views import View
from BackendWork.forms import *
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse, HttpResponseForbidden, HttpResponse
from BackendWork.models import *
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm


class UserLoginView(View):
    @staticmethod
    def get(request):
        return render(request, 'login.html')

    @staticmethod
    def post(request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page
            return redirect('/')
        else:
            # Return an 'invalid login' error message.
            return render(request, 'login.html', {'error': 'Invalid login credentials.'}, status=401)


# accounts/views.py

class UserRegisterView(View):
    @staticmethod
    def get(request):
        return render(request, 'register.html')

    @staticmethod
    def post(request):
        data = json.loads(request.body)
        username = data.get('username')
        email = data.get('email')
        password1 = data.get('password1')
        password2 = data.get('password2')

        form_data = {
            'email': email,
            'username': username,
            'password1': password1,
            'password2': password2,  # Assuming you want both password fields to have the same value
        }

        form = UserCreationForm(form_data)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Account Registered! Redirecting you to login to sign in...'}, status=200)
        else:
            return JsonResponse({'message': form.errors}, status=401)


class AccountManagementView(View):
    @staticmethod
    @login_required(login_url='/login/')
    def get(request):
        user = request.user
        form = UserChangeForm(instance=user)
        return render(request, 'account_management.html', {'form': form})

    @staticmethod
    @login_required(login_url='/login/')
    def post(request):
        data = json.loads(request.body)
        username = data.get('username')
        email = data.get('email')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        phone_number = data.get('phone_number')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User does not exist'}, status=404)

        if user != request.user:
            return JsonResponse({'error': 'You are not authorized to update this user'}, status=403)

        user.first_name = first_name
        user.last_name = last_name
        user.phone_number = phone_number
        user.save()

        return JsonResponse({'message': 'Account Information Updated!!!'}, status=200)


class AccountCartView(View):
    @staticmethod
    @login_required(login_url='/login/')
    def get(request):
        cart = request.user.cart
        return render(request, 'cart.html', {'cartItems': cart.get_cart_items,
                                             'cartCount': cart.cart_summary['total_count'],
                                             'cartTotal': cart.cart_summary['subtotal']})


# @staticmethod
# @login_required(login_url='/login/')
# def post(request):
#     data = json.loads(request.body)
#     name = data.get('name')
#     card = data.get('card')
#     expiration = data.get('expiration')
#     back = data.get('back_number')
#
#     form_data = {
#         'name': name,
#         'card_number': card,
#         'expiration_date': expiration,
#         'back_number': back,
#     }
#
#     form = CardCreationForm(form_data)
#     if form.is_valid():
#         return JsonResponse({'message': 'Card success! Redirecting you to home page...'}, status=200)
#     else:
#         return JsonResponse({'message': form.errors}, status=401)


def updateCartQty(request):
    if request.method == 'POST':
        user_cart = get_object_or_404(Cart, user=request.user)
        newQty = int(request.POST.get('newQty'))

        cartItem = get_object_or_404(CartItem, cart=user_cart, product=request.POST.get('productId'))
        cartItem.quantity = newQty
        cartItem.save()

    return redirect('AccountCartView')


def home(request):
    products = Product.objects.all()
    categories = Product.CATEGORY_CHOICES.items()
    return render(request, 'home.html', {'products': products, 'categories': categories})


def categoryFilter(request, category):
    products = Product.objects.filter(category=category)
    categories = Product.CATEGORY_CHOICES.items()
    return render(request, 'home.html', {'products': products, 'categories': categories})



def search(request):
    filters = request.GET.getlist('filters')
    query = request.GET.get('searchQuery')
    searchWords = query.split()

    products = Product.objects.all()
    filteredProducts = []

    for searchWord in searchWords:
        for filter in filters:
            if filter == 'store':
                filteredProducts.extend(products.filter(soldByStoreId__name__contains=searchWord))
            if filter == 'name':
                filteredProducts.extend(products.filter(name__contains=searchWord))
            if filter == 'category':
                filteredProducts.extend(products.filter(category__contains=searchWord))


    # Remove duplicates by converting filteredProducts to a set and then back to a list
    filteredProducts = list(set(filteredProducts))

    categories = Product.CATEGORY_CHOICES.items()
    return render(request, 'home.html', {'products': filteredProducts, 'categories': categories})

def removeFavorite(request):
    data = json.loads(request.body)
    favorite_id = data['favorite_id']
    product = get_object_or_404(Product, productId=favorite_id)
    user = User.objects.get(username=request.user)
    user.favorite.remove(product)
    user.save()
    print('Favorite product removed!')
    return JsonResponse({'message': 'Favorite product removed!'}, status=200)


def addFavorite(request):
    data = json.loads(request.body)
    favorite_id = data['favorite_id']
    product = get_object_or_404(Product, productId=favorite_id)
    user = User.objects.get(username=request.user)
    user.favorite.add(product)
    user.save()
    print('Favorite product added!')
    return JsonResponse({'message': 'Favorite product added!'}, status=200)



class StorefrontView(View):
    @staticmethod
    def get(request):
        user = request.user
        store = Storefront.objects.filter(owner=user).first()
        products = Product.objects.filter(soldByStoreId=store)
        orders = Order.objects.filter(seller=user)
        return render(request, 'storefront.html', {'store': store, 'products': products, 'orders': orders})

    @staticmethod
    def post(request):
        user = request.user
        store = Storefront.objects.filter(owner=user).first()
        store_name = request.POST.get('storeName')
        store_description = request.POST.get('storeDescription')
        banner_input = request.FILES.get('bannerInput')
        logo_input = request.FILES.get('logoInput')

        store.name = store_name
        store.description = store_description
        store.bannerImage = banner_input
        store.logoImage = logo_input
        store.save()

        return JsonResponse({'success': True, 'message': 'Changes confirmed successfully'})


class VendorView(View):
    @staticmethod
    def get(request, store_id):
        store = Storefront.objects.filter(storeId=store_id).first()
        products = Product.objects.filter(soldByStoreId_id=store_id)
        return render(request, 'vendor.html', {'products': products, 'store': store})


def createproduct(request):
    return render(request, 'createproduct.html')


def custom_logout(request):
    logout(request)
    return redirect('/')


class ProductDetailView(View):
    @staticmethod
    def get(request, product_id):
        product = get_object_or_404(Product, productId=product_id)
        reviews = ProductReviews.objects.filter(productId=product.productId)
        favorite = User.objects.filter(id=request.user.id, favorite=product.productId).exists()
        return render(request, 'product_detail.html', {'product': product, 'reviews': reviews,
                                                       'favorite': favorite})

    # @staticmethod
    # @login_required(login_url='/login/')
    # def post(request, product_id):
    #     data = json.loads(request.body)
    #     quantity = data.get('quantity')
    #     cart = {} #Invoice.objects.get(customerId=request.user.id, orderStatus='C1')
    #     product = get_object_or_404(Product, productId=product_id)
    #
    #     # try:
    #     #     addingProduct = LineItem.objects.get(invoiceId=cart.invoiceId, productId=product.productId)
    #     # except LineItem.DoesNotExist:
    #     #     form_data = {
    #     #         'invoiceId': cart.invoiceId,
    #     #         'productId': product.productId,
    #     #         'quantity': quantity,
    #     #         'linePrice': 1,
    #     #     }
    #     #     form = LineItemCreationForm(form_data)
    #
    #         print("Form is created here")
    #
    #         if form.is_valid():
    #             form.save();
    #             return JsonResponse({'message': 'Card success! Redirecting you to home page...'}, status=200)
    #         else:
    #             return JsonResponse({'message': form.errors}, status=401)
    #
    #     addingProduct.quantity += int(quantity)
    #     addingProduct.save()
    #     return JsonResponse({'message': 'Card success! Redirecting you to home page...'}, status=200)


class UpdateProductView(LoginRequiredMixin, View):
    @staticmethod
    def get(request, product_id):
        product = get_object_or_404(Product, productId=product_id)

        if request.user == product.soldByStoreId.owner:
            # Render the product update page
            return render(request, 'edit_product.html', {'product': product})
        else:
            return HttpResponseForbidden("You are not authorized to access this page.")

    @staticmethod
    def post(request, product_id):
        product = get_object_or_404(Product, productId=product_id)

        if request.user == product.soldByStoreId.owner:
            data = json.loads(request.body)
            name = data.get('product_name')
            price = data.get('price')
            description = data.get('description')
            qoh = data.get('qoh')

            if name:
                product.name = name
            if price:
                product.price = price
            if description:
                product.description = description
            if qoh:
                product.qoh = qoh
            product.save()

            return JsonResponse({'message': 'Product Information Updated!!!'}, status=200)

        else:
            return HttpResponseForbidden("You are not authorized to access this page.")


class AddProductView(View):
    @staticmethod
    @login_required(login_url='/login/')
    def get(request, store_id):
        return render(request, 'addproduct.html')

    @staticmethod
    @login_required(login_url='/login/')
    def post(request, store_id):
        productData = json.loads(request.body)

        form_data = {
            'soldByStoreId': store_id,
            'name': productData.get('name'),
            'description': productData.get('description'),
            'price': productData.get('price'),
            'qoh': productData.get('qoh'),
            'category': productData.get('category'),
            'weight': productData.get('weight'),
            'length': productData.get('length'),
            'width': productData.get('width'),
            'height': productData.get('height'),
            'image': productData.get('image')
        }

        form = AddProductForm(form_data)

        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Product created! Redirecting you to storefront...'}, status=200)
        else:
            return JsonResponse({'message': form.errors}, status=401)


class ReviewProductView(View):
    @staticmethod
    @login_required(login_url='/login/')
    def get(request, product_id):
        product = get_object_or_404(Product, productId=product_id)
        storefront = product.soldByStoreId.name
        return render(request, 'review_product.html', {'product': product, 'username': request.user,
                                                       'storefront': storefront})

    @staticmethod
    @login_required(login_url='/login/')
    def post(request, product_id):
        reviewData = json.loads(request.body)

        product = get_object_or_404(Product, productId=product_id)
        rating = reviewData.get('rating')
        comment = reviewData.get('comment')

        ProductReviews.objects.create(productId=product, reviewerId=request.user, rating=rating,
                                      comment=comment)
        # return redirect(f'/products/{product_id}')
        # return redirect('/')
        # return ProductDetailView.get(request, product_id)
        return JsonResponse({'message': 'Review created! Redirecting to product detail page...'}, status=200)

def deleteProduct(request, productid):
    get_object_or_404(Product, id=productid)
    Product.objects.filter(productId=productid).delete()
    return redirect('storefront/')
    # I assume it should redirect to the storefront, but I'm not entirely sure. Can just change this if it's wrong


class ProductDeleteView(View):

    @staticmethod
    # @login_required(login_url='/login/')
    def post(request, productid):
        Product.objects.filter(productId=productid).delete()


class SavedProductView(View):
    @staticmethod
    @login_required(login_url='/login')
    def get(request):
        favorite = User.objects.get(id=request.user.id).favorite.all()
        return render(request, 'favorite.html', {'favorites': favorite})


@login_required(login_url='/login/')
def checkout_view(request):
    host = request.get_host()
    cart = request.user.cart

    invoice = Invoice.objects.create(user=request.user)

    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': cart.cart_summary['subtotal'],
        'item_name': 'Order-Item-No-{}'.format(invoice.invoiceId),
        'invoice': 'Invoice-No-{}'.format(invoice.invoiceId),
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format(host, reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host, '/payment-completed/{}'.format(invoice.invoiceId)),
        'cancel_url': 'http://{}{}'.format(host, '/payment-failed/{}'.format(invoice.invoiceId)),
    }

    paypay_payment_button = CustomPayPalPaymentsForm(initial=paypal_dict)

    return render(request, 'checkout.html', {'paypay_payment_button': paypay_payment_button,
                                             'cartItems': cart.get_cart_items,
                                             'cartCount': cart.cart_summary['total_count'],
                                             'cartTotal': cart.cart_summary['subtotal'],
                                             'state_choices': STATE_CHOICES})


def payment_complete_view(request, invoice_id):
    payer_id = request.GET.get('PayerID')
    cart = request.user.cart
    invoice = Invoice.objects.get(pk=invoice_id)

    if invoice.get_invoice_items.count() == 0:
        for cart_item in cart.get_cart_items:
            InvoiceItem.objects.create(invoice=invoice, product=cart_item.product, quantity=cart_item.quantity)
            sellers = cart.sellers_in_cart

        for seller in sellers:
            order = Order.objects.create(seller=seller, customer=request.user)
            for cart_item in cart.get_cart_items:
                OrderItem.objects.create(order=order, product=cart_item.product, quantity=cart_item.quantity)

        cart.clear_cart()

        return render(request, 'payment-completed.html', {
                                             'cartItems': invoice.get_invoice_items,
                                             'cartCount': invoice.invoice_summary['total_count'],
                                             'cartTotal': invoice.invoice_summary['subtotal']})
    else:
        return render(request, 'payment-completed.html', {
            'cartItems': cart.get_cart_items,
            'cartCount': cart.invoice_summary['total_count'],
            'cartTotal': cart.invoice_summary['subtotal']})


def payment_failed_view(request):
    return render(request, 'payment-failed.html')


def update_favorite(request):
    return render(request, 'product_card.html')
