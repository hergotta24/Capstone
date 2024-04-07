from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone


# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=10, null=True, blank=True)

    # Methods to support favoriting/unfavoriting products
    def add_favorite(self, product):
        Favorite.objects.get_or_create(user=self, product=product)

    def remove_favorite(self, product):
        Favorite.objects.filter(user=self, product=product).delete()

    def has_favorite(self, product):
        return Favorite.objects.filter(user=self, product=product).exists()

    def get_favorites(self):
        return Product.objects.filter(favorite__user=self)


class Favorite(models.Model):
    favoriteId = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username} (ID {self.user.id}), {self.product.name} (ID {self.product.productId})"


STATE_CHOICES = {('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('CA', 'California'),
                 ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('DC', 'District of Columbia'),
                 ('FL', 'Florida'), ('GA', 'Georgia'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'),
                 ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'),
                 ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'),
                 ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'),
                 ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'),
                 ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'),
                 ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'),
                 ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'),
                 ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VA', 'Virginia'), ('WA', 'Washington'),
                 ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming'), ('AS', 'American Samoa'),
                 ('GU', 'Guam'), ('MP', 'Northern Mariana Islands'), ('PR', 'Puerto Rico'), ('VI', 'Virgin Islands')
                 }


class Address(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    addressId = models.AutoField(primary_key=True)
    line1 = models.CharField(max_length=50)
    line2 = models.CharField(max_length=50, blank=True, null=True)
    aptNum = models.CharField(max_length=10, blank=True, null=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=2, choices=STATE_CHOICES)
    zipCode = models.CharField(max_length=5)


class Storefront(models.Model):
    storeId = models.AutoField(primary_key=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500, null=True)
    dateCreated = models.DateTimeField(auto_now_add=True)
    bannerImage = models.ImageField(upload_to='storefront_banners/', null=True, blank=True)
    logoImage = models.ImageField(upload_to='storefront_logos/', null=True, blank=True)


class StoreReviews(models.Model):
    reviewId = models.AutoField(primary_key=True)
    storeId = models.ForeignKey(Storefront, on_delete=models.CASCADE)
    reviewerId = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    rating = models.PositiveIntegerField()
    comment = models.CharField(max_length=500)
    reviewDate = models.DateTimeField(auto_now_add=True)


class Product(models.Model):
    class Meta:
        unique_together = ['name', 'soldByStoreId']

    CATEGORY_CHOICES = {'arts_crafts': 'Arts & Crafts Supplies', 'automotive': 'Automotive & Tools',
                        'children': 'Baby & Kids', 'beauty': 'Beauty & Personal Care', 'books': 'Books & Stationery',
                        'clothing': 'Clothing & Apparel', 'electronics': 'Electronics', 'fitness': 'Fitness & Exercise',
                        'furniture_decor': 'Furniture & Decor', 'outdoors': 'Gardening & Outdoor Living',
                        'health_wellness': 'Health & Wellness', 'jewelry': 'Jewelry & Accessories',
                        'office': 'Office Supplies', 'pets': 'Pet Supplies', 'sports': 'Sports & Outdoors',
                        'toys': 'Toys & Games', 'travel': 'Travel & Luggage'}

    productId = models.AutoField(primary_key=True)
    soldByStoreId = models.ForeignKey(Storefront, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=1000)
    price = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0.01)])
    qoh = models.PositiveIntegerField(default=0, verbose_name='Quantity on Hand')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    weight = models.FloatField(validators=[MinValueValidator(0.01)])
    length = models.FloatField(validators=[MinValueValidator(0.01)])
    width = models.FloatField(validators=[MinValueValidator(0.01)])
    height = models.FloatField(validators=[MinValueValidator(0.01)])
    dateAdded = models.DateTimeField(auto_now_add=True)

    @property
    def images(self):
        return self.product_image.all()

    @property
    def thumbnail(self):
        return self.product_image.first()


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_image')
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='product_images/')


class ProductReviews(models.Model):
    reviewId = models.AutoField(primary_key=True)
    productId = models.ForeignKey(Product, on_delete=models.CASCADE)
    reviewerId = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    rating = models.PositiveIntegerField()
    comment = models.CharField(max_length=500)
    reviewDate = models.DateTimeField(auto_now_add=True)


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='CartItem')

    @property
    def get_cart_items(self):
        return self.cart_item.all()

    @property
    def cart_summary(self):
        total_count = 0
        subtotal = 0
        cart_items = self.get_cart_items
        for item in cart_items:
            total_count += item.quantity
            subtotal += item.total_price
        return {'total_count': total_count, 'subtotal': subtotal}

    def clear_cart(self):
        self.cart_item.all().delete()

    @property
    def sellers_in_cart(self):
        sellers = set()
        cart_items = self.get_cart_items
        for item in cart_items:
            sellers.add(item.product.soldByStoreId.owner)
        return list(sellers)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_item')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_price(self):
        return self.quantity * self.product.price


class Invoice(models.Model):
    invoiceId = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invoices')
    products = models.ManyToManyField(Product, through='InvoiceItem')

    @property
    def get_invoice_items(self):
        return self.invoice_item.all()

    @property
    def invoice_summary(self):
        total_count = 0
        subtotal = 0
        cart_items = self.invoice_item.all()
        for item in cart_items:
            total_count += item.quantity
            subtotal += item.total_price
        return {'total_count': total_count, 'subtotal': subtotal}


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='invoice_item')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_price(self):
        return self.quantity * self.product.price


class Order(models.Model):
    orderId = models.AutoField(primary_key=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller_orders')
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer_orders')
    products = models.ManyToManyField(Product, through='OrderItem')
    shippingAddress = models.ForeignKey(Address, on_delete=models.CASCADE, null=True)

    @property
    def get_order_items(self):
        return self.order_item.all()

    @property
    def order_summary(self):
        total_count = 0
        subtotal = 0
        order_item = self.order_item.all()
        for item in order_item:
            total_count += item.quantity
            subtotal += item.total_price
        return {'total_count': total_count, 'subtotal': subtotal}


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_item')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_price(self):
        return self.quantity * self.product.price
