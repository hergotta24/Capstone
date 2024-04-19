from _ast import Store

from django.contrib.auth import authenticate, login, logout
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, TopPadder
from verify_email.email_handler import send_verification_email
from django.core.mail import send_mail
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
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
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
            inactive_user = send_verification_email(request, form)
            Cart.objects.create(user=inactive_user)
            Storefront.objects.create(owner=inactive_user, name=username + '\'s Store', description='')
            user = User.objects.get(email=email)
            # Cart.objects.create(user=user)
            Storefront.objects.create(owner=user)
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


def updateCartQty(request):
    if request.method == 'POST':
        user_cart = get_object_or_404(Cart, user=request.user)
        updateData = json.loads(request.body)
        newQty = int(updateData.get('newQty'))
        cartItem = get_object_or_404(CartItem, cart=user_cart, product=updateData.get('productId'))
        cartItem.quantity = newQty
        cartItem.save()

    return JsonResponse({'message': 'Quantity updated! Refreshing shopping cart page...'}, status=200)


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

        if not request.user.is_anonymous:
            ordered = Product.objects.filter(productId=product_id, orderitem__order__customer=request.user).exists()
            reviewed = ProductReviews.objects.filter(productId=product_id, reviewerId=request.user).first()
            # reviews = reviews.exclude(reviewerId=request.user)

            return render(request, 'product_detail.html', {'product': product, 'reviews': reviews,
                                                           'favorite': favorite, 'ordered': ordered,
                                                           'reviewed': reviewed})
        else:
            return render(request, 'product_detail.html', {'product': product, 'reviews': reviews})

    @staticmethod
    @login_required(login_url='/login/')
    def post(request, product_id):
        data = json.loads(request.body)
        quantity = int(data.get('quantity'))
        user_cart = Cart.objects.get(user=request.user)
        product = get_object_or_404(Product, productId=product_id)
        cart_item, cart_item_created = CartItem.objects.get_or_create(cart=user_cart, product=product)
        if not cart_item_created:
            # If the cart item already exists, update the quantity
            cart_item.quantity += quantity
            cart_item.save()
        else:
            # If the cart item is newly created, set the quantity
            cart_item.quantity = quantity
            cart_item.save()
        return JsonResponse({'message': 'Added Product to Cart'}, status=200)


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
        return render(request, 'product-creation.html', {'store_id': store_id})

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
            'weight': 1,
            'length': 1,
            'width': 1,
            'height': 1,
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
        if rating == 0:
            return JsonResponse({'message': 'Rating required'}, status=400)
        if comment == '':
            return JsonResponse({'message': 'Comment required'}, status=400)
        reviewer = User.objects.get(username=request.user)
        ProductReviews.objects.create(productId=product, reviewerId=reviewer, rating=rating,
                                      comment=comment)

        return JsonResponse({'message': 'Review created! Redirecting to product detail page...'}, status=200)


def deleteProduct(request, productid):
    get_object_or_404(Product, id=productid)
    Product.objects.filter(productId=productid).delete()
    return redirect('storefront/')
    # I assume it should redirect to the storefront, but I'm not entirely sure. Can just change this if it's wrong


def removeFromCart(request, product_id):
    cart = get_object_or_404(Cart, user=request.user)
    product = get_object_or_404(Product, productId=product_id)
    CartItem.objects.get(cart=cart, product=product).delete()
    return redirect('/cart/')


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
        return render(request, 'favorite.html', {'products': favorite})


@login_required(login_url='/login/')
def checkout_view(request):
    cart = request.user.cart
    Invoice.objects.get_or_create(user=request.user, invoice_status='PENDING')
    if cart.get_cart_items.count() > 0:
        return render(request, 'checkout.html',
                      {'cartItems': cart.get_cart_items,
                       'cartCount': cart.cart_summary['total_count'],
                       'cartTotal': cart.cart_summary['subtotal'],
                       'state_choices': STATE_CHOICES,
                       })
    else:
        print('ERROR: No Items in Cart!!!!')
        return render(request, 'home.html')


def payment_complete_view(request, invoice_id):
    payer_id = request.GET.get('PayerID')
    cart = request.user.cart
    invoice = Invoice.objects.get(pk=invoice_id, user=request.user)
    print(invoice.invoice_status)
    if invoice.invoice_status == 'COMPLETED':
        return render(request, 'payment-completed.html', {
            'cartItems': invoice.get_invoice_items,
            'cartCount': invoice.invoice_summary['total_count'],
            'cartTotal': invoice.invoice_summary['subtotal'],
            'invoiceId': invoice_id})

    # TODO Could also include the payer_id to make this more secure...
    #  However to make it easier to debug I'm leaving it out
    if invoice.invoice_status == "PENDING":
        for cart_item in cart.get_cart_items:
            InvoiceItem.objects.create(invoice=invoice, product=cart_item.product, quantity=cart_item.quantity)
            sellers = cart.sellers_in_cart

        for seller in sellers:
            order = Order.objects.create(seller=seller, customer=request.user)
            for cart_item in cart.get_cart_items:
                OrderItem.objects.create(order=order, product=cart_item.product, quantity=cart_item.quantity)

        invoice.invoice_status = 'COMPLETED'
        invoice.save()

        if invoice.shippingAddress is not None:
            order.shippingAddress = invoice.shippingAddress
            order.save()
        cart.clear_cart()

        return render(request, 'payment-completed.html', {
            'cartItems': invoice.get_invoice_items,
            'cartCount': invoice.invoice_summary['total_count'],
            'cartTotal': invoice.invoice_summary['subtotal']})
    else:
        print("Error: Invoice State isn't set")
        products = Product.objects.all()
        categories = Product.CATEGORY_CHOICES.items()
        return render(request, 'home.html', {'products': products, 'categories': categories})


def payment_failed_view(request):
    return render(request, 'payment-failed.html')


class OrderHistoryView(View):
    @staticmethod
    @login_required(login_url='/login/')
    def get(request):
        user = request.user
        invoices = Invoice.objects.filter(user=user, invoice_status="COMPLETED")
        return render(request, 'order_history.html', {'invoices': invoices})


def update_favorite(request):
    return render(request, 'product_card.html')


def generate_invoice_pdf(request, invoice_id):
    # Retrieve order details (Sold To, Shipped To, Item Details, etc.) based on order_id
    invoice = Invoice.objects.filter(invoiceId=invoice_id).first()
    sold_to = str(invoice.user)
    shipped_to = invoice.shippingAddress
    address_lines = shipped_to.line1
    if shipped_to.line2:
        address_lines.append(" " + shipped_to.line2)
    if shipped_to.aptNum:
        address_lines.append(" " + shipped_to.aptNum)
    items = invoice.get_invoice_items
    subtotal = invoice.invoice_summary['subtotal']

    # Generate PDF document
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=invoice_{invoice_id}.pdf'

    # Create PDF document using SimpleDocTemplate
    pdf = SimpleDocTemplate(response, pagesize=letter)

    # Define sample data (replace with actual data)
    invoice_id = invoice_id
    invoice_date = invoice.get_date

    # Define content elements
    content = []
    styles = getSampleStyleSheet()
    bold_style = ParagraphStyle(
        name='Bold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
    )

    # Define a custom style for right-aligned content
    right_aligned_style = ParagraphStyle(
        "right_aligned",
        parent=styles["Normal"],
        alignment=2,  # 0=Left, 1=Center, 2=Right
    )

    right_aligned_title = ParagraphStyle(
        "right_title",
        parent=styles["Title"],
        alignment=2,
    )

    left_aligned_title = ParagraphStyle(
        "left_title",
        parent=styles["Title"],
        alignment=0,
    )

    content.append(Paragraph("ShopSavvy", left_aligned_title))
    content.append(Spacer(1, -20))
    content.append(Paragraph("INVOICE", right_aligned_title))

    content.append(Spacer(1, 40))  # Spacer for vertical space

    # Right-aligned content for Invoice ID and Invoice Date
    content.append(Paragraph(f'Invoice ID: {invoice_id}', right_aligned_style))
    content.append(Paragraph(f'Invoice Date: {invoice_date}', right_aligned_style))

    content.append(Spacer(1, -20))  # Spacer for vertical space

    content.append(Paragraph("Sold To:", bold_style))
    content.append(Paragraph(sold_to, styles['Normal']))

    content.append(Spacer(1, 20))  # Spacer for vertical space

    content.append(Paragraph("Shipped To:", bold_style))
    content.append(Paragraph(address_lines, styles['Normal']))
    content.append(Paragraph(f'{shipped_to.city}, {shipped_to.state} {shipped_to.zipCode}', styles['Normal']))

    content.append(Spacer(1, 40))  # Spacer for vertical space

    content.append(Paragraph("Item Details:", bold_style))
    # Add more content for item details if needed

    # Build PDF document with the content elements
    data = [["PRODUCT", "SELLER", "QUANTITY", "UNIT PRICE", "AMOUNT"]]
    for item in items:
        data.append(
            [f'{item.product.name}', f'{item.product.soldByStoreId.owner}', f'{item.quantity}', f'{item.product.price}',
             f'${item.total_price}'])
    data.append(['', '', '', '', ''])
    data.append(['', '', '', 'SUBTOTAL', f'${subtotal}'])
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),  # Background color for header row
        ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black),  # Bottom border for header row
        ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Bottom border for header row
        ('LINEBELOW', (0, 1), (-1, -1), 0, colors.white),  # Remove inner borders
        ('BOX', (0, 0), (-1, -1), 1, colors.black),  # Outer border for the entire table
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center alignment for all cells
        # ('SPAN', (-1, 0), (-1, 2)),
        ('VALIGN', (-1, 0), (-1, -1), 'BOTTOM'),
    ])


    table = Table(data, colWidths=[140, 100, 80, 90, 90], style=table_style)
    content.append(table)
    pdf.build(content)
    # pdf.save()
    return response


def add_shipping_details(request):
    if request.method == 'POST':
        try:
            # Retrieve form data
            host = request.get_host()
            email = request.POST.get('email')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            address_line_1 = request.POST.get('address-line-1')
            address_line_2 = request.POST.get('address-line-2')
            city = request.POST.get('city')
            state = request.POST.get('state')
            address_zipCode = request.POST.get('address-zipCode')
            phone_number = request.POST.get('phone_number')

            # Check if all required fields are filled
            if email and first_name and last_name and address_line_1 and city and state and address_zipCode:
                user = request.user

                # Check if there's an existing shipping address for the user
                invoice = Invoice.objects.get(user=user, invoice_status='PENDING')
                if invoice.shippingAddress:
                    prevAddy = invoice.shippingAddress
                    prevAddy.delete()

                # Create Address object and save to database
                shipping_address = Address.objects.create(
                    line1=address_line_1,
                    line2=address_line_2,
                    city=city,
                    state=state,
                    zipCode=address_zipCode,
                )

                # Add the user to the address
                shipping_address.user.add(user)

                # Associate the shipping address with the invoice
                invoice.shippingAddress = shipping_address
                invoice.save()

                paypal_dict = {
                    'business': settings.PAYPAL_RECEIVER_EMAIL,
                    'amount': user.cart.cart_summary['subtotal'],
                    'item_name': 'Order-Item-No-{}'.format(invoice.invoiceId),
                    'invoice': 'Invoice-No-{}'.format(invoice.invoiceId),
                    'currency_code': 'USD',
                    'notify_url': 'http://{}{}'.format(host, reverse('paypal-ipn')),
                    'return_url': 'http://{}{}'.format(host, '/payment-completed/{}'.format(invoice.invoiceId)),
                    'cancel_url': 'http://{}{}'.format(host, '/payment-failed/{}'.format(invoice.invoiceId)),
                }

                paypay_payment_button = CustomPayPalPaymentsForm(initial=paypal_dict)

                return JsonResponse({'message': 'Shipping details added successfully',
                                     'buyNowButton': paypay_payment_button.render()}, status=200)
            else:
                return JsonResponse({'error': 'Missing required fields'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


def removeFromCart(request, product_id):
    cart = get_object_or_404(Cart, user=request.user)
    product = get_object_or_404(Product, productId=product_id)
    CartItem.objects.get(cart=cart, product=product).delete()
    return redirect('/cart/')
