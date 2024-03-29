from django.contrib.auth import authenticate, login, logout
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.views import View
from BackendWork.forms import *
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse, HttpResponseForbidden
from BackendWork.models import User, Product, Storefront, Invoice, LineItem, ProductReviews
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.uploadedfile import SimpleUploadedFile


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
        invoiceNumber = Invoice.objects.get(customerId=request.user.id, orderStatus='C1')
        user_cart = LineItem.objects.filter(invoiceId=invoiceNumber)
        subtotal = 0.00
        for y in user_cart:
            subtotal += float(y.productId.price)
        tax = round(subtotal * 0.082, 2)
        shipping = 20.00
        discount = 1.00
        total = subtotal + tax + shipping
        return render(request, 'cart.html',
                      {"cart": user_cart, "subtotal": format(subtotal, '0.2f'), "tax": format(tax, '0.2f')
                          , "shipping": format(shipping, '0.2f'), "discount": format(discount, '0.2f'),
                       "total": format(total, '0.2f')})

    @staticmethod
    @login_required(login_url='/login/')
    def post(request):
        data = json.loads(request.body)
        name = data.get('name')
        card = data.get('card')
        expiration = data.get('expiration')
        back = data.get('back_number')

        form_data = {
            'name': name,
            'card_number': card,
            'expiration_date': expiration,
            'back_number': back,
        }

        form = CardCreationForm(form_data)
        if form.is_valid():
            return JsonResponse({'message': 'Card success! Redirecting you to home page...'}, status=200)
        else:
            return JsonResponse({'message': form.errors}, status=401)


def home(request):
    products = Product.objects.all()
    categories = Product.CATEGORY_CHOICES.items()
    return render(request, 'home.html', {'products': products, 'categories': categories})


def categoryFilter(request, category):
    products = Product.objects.filter(category=category)
    categories = Product.CATEGORY_CHOICES.items()
    return render(request, 'home.html', {'products': products, 'categories': categories})


class StorefrontView(View):
    @staticmethod
    def get(request):
        user = request.user
        store = Storefront.objects.filter(owner=user).first()
        products = Product.objects.filter(soldByStoreId=store)
        return render(request, 'storefront.html', {'store': store, 'products': products})

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
        store.bannerInput = banner_input
        store.logoInput = logo_input
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
        return render(request, 'product_detail.html', {'product': product, 'reviews': reviews})

    @staticmethod
    @login_required(login_url='/login/')
    def post(request, product_id):
        data = json.loads(request.body)
        quantity = data.get('quantity')
        cart = Invoice.objects.get(customerId=request.user.id, orderStatus='C1')
        product = get_object_or_404(Product, productId=product_id)

        try:
            addingProduct = LineItem.objects.get(invoiceId=cart.invoiceId, productId=product.productId)
        except LineItem.DoesNotExist:
            form_data = {
                'invoiceId': cart.invoiceId,
                'productId': product.productId,
                'quantity': quantity,
                'linePrice': 1,
            }
            form = LineItemCreationForm(form_data)

            print("Form is created here")

            if form.is_valid():
                form.save();
                return JsonResponse({'message': 'Card success! Redirecting you to home page...'}, status=200)
            else:
                return JsonResponse({'message': form.errors}, status=401)

        addingProduct.quantity += int(quantity)
        addingProduct.save()
        return JsonResponse({'message': 'Card success! Redirecting you to home page...'}, status=200)


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
