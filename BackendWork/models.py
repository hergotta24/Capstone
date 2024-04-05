from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone


# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=10, null=True, blank=True)
    shipping_address = models.ForeignKey('Address', on_delete=models.SET_NULL, null=True,
                                         related_name="userShippingAddress", blank=True)
    billing_address = models.ForeignKey('Address', on_delete=models.SET_NULL, null=True,
                                        related_name="userBillingAddress", blank=True)
    payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, null=True,
                                related_name="paymentMethod", blank=True)
    favorite = models.ManyToManyField('Product')

class Payment(models.Model):
    name = models.CharField(max_length=100)
    card_number = models.CharField(max_length=16)
    expiration_date = models.CharField(max_length=4)
    back_number = models.CharField(max_length=3)


class Address(models.Model):
    STATE_CHOICES = [('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('CA', 'California'),
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
                     ]

    addressId = models.AutoField(primary_key=True)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    line1 = models.CharField(max_length=50)
    line2 = models.CharField(max_length=50, blank=True, null=True),
    aptNum = models.CharField(max_length=10, null=True)
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


class Invoice(models.Model):
    ORDER_STATUS = [('C1', 'Cart'), ('C2', 'Completed')]
    invoiceId = models.AutoField(primary_key=True)
    customerId = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    storeId = models.ForeignKey(Storefront, on_delete=models.SET_NULL, null=True)
    subtotal = models.DecimalField(max_digits=8, decimal_places=2)
    discount = models.DecimalField(max_digits=8, decimal_places=2)
    tax = models.DecimalField(max_digits=8, decimal_places=2)
    shipping = models.CharField(max_length=2, choices=ORDER_STATUS)
    orderStatus = models.CharField(max_length=20)
    invoiceDate = models.DateTimeField(auto_now_add=True)


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


class LineItem(models.Model):
    lineItemId = models.AutoField(primary_key=True)
    invoiceId = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    productId = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField()
    linePrice = models.DecimalField(max_digits=8, decimal_places=2)


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


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_item')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_price(self):
        return self.quantity * self.product.price
