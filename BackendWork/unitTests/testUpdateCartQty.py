from decimal import Decimal

from django.test import TestCase, Client

from BackendWork.models import User, Storefront, Product, Cart, CartItem


class TestUpdateCartQty(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='testUser', password='p@55w0rD', email='testuser@gmail.com')
        self.storefront1 = Storefront.objects.create(owner=self.user1, name='Test Storefront')
        self.product1 = Product.objects.create(soldByStoreId=self.storefront1, name='Test Product',
                                               description='Description', price=9.99, qoh=99, weight=1.0, length=1.0,
                                               width=1.0, height=1.0)
        self.product2 = Product.objects.create(soldByStoreId=self.storefront1, name='Test Product2',
                                               description='Description', price=42.42, qoh=99, weight=1.0, length=1.0,
                                               width=1.0, height=1.0)
        self.cart1 = Cart.objects.create(user=self.user1)
        self.cart1.add_product(self.product1, 1)
        self.cart1.add_product(self.product2, 2)
        self.client.login(username='testUser', password='p@55w0rD')

    def testUpdateQty(self):
        response = self.client.post('/updateCartQty/', data={'productId': self.product1.productId, 'newQty': 37})
        self.assertRedirects(response, '/cart/')

        userCart = Cart.objects.get(user=self.user1)
        cartItem = CartItem.objects.get(cart=userCart, product=self.product1.productId)

        self.assertEqual(37, cartItem.quantity)
        self.assertEqual(37 * cartItem.product.price, cartItem.total_price)
        self.assertEqual(userCart.cart_summary['subtotal'], Decimal(str(self.product1.price * 37 + self.product2.price * 2)))



