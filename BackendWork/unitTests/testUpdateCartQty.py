from decimal import Decimal

from django.test import TestCase, Client

from BackendWork.models import User, Storefront, Product, Invoice, LineItem


class TestUpdateCartQty(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='testUser', password='p@55w0rD', email='testuser@gmail.com')
        self.user2 = User.objects.create_user(username='testUser2', password='p@55w0rD', email='testuser2@gmail.com')
        self.storefront1 = Storefront.objects.create(owner=self.user1, name='Test Storefront')
        self.product1 = Product.objects.create(soldByStoreId=self.storefront1, name='Test Product',
                                               description='Description', price=9.99, qoh=99, weight=1.0, length=1.0,
                                               width=1.0, height=1.0)
        self.product2 = Product.objects.create(soldByStoreId=self.storefront1, name='Test Product2',
                                               description='Description', price=42.42, qoh=99, weight=1.0, length=1.0,
                                               width=1.0, height=1.0)
        self.invoice1 = Invoice.objects.create(customerId=self.user1, storeId=self.storefront1, orderStatus='C1')
        self.qty1 = 1
        self.qty2 = 2
        self.lineItem1 = LineItem.objects.create(invoiceId=self.invoice1, productId=self.product1, quantity=self.qty1,
                                                 linePrice=(self.qty1 * self.product1.price))
        self.lineItem2 = LineItem.objects.create(invoiceId=self.invoice1, productId=self.product2, quantity=self.qty2,
                                                 linePrice=(self.qty2 * self.product2.price))
        # self.invoice1.subtotal = self.product1.price * self.qty1 + self.product2.price * self.qty2
        self.invoice1.subtotal = self.lineItem1.linePrice + self.lineItem2.linePrice
        self.invoice1.tax = self.invoice1.subtotal * 0.056
        self.client.login(username='testUser', password='p@55w0rD')

    def testUpdateQty(self):
        response = self.client.post('/updateCartQty/', data={'productId': self.lineItem1.productId_id, 'newQty': 37})
        cartItem = LineItem.objects.get(productId=self.lineItem1.productId_id)
        invoice = cartItem.invoiceId
        self.assertEqual(37, cartItem.quantity)
        self.assertEqual(37 * cartItem.productId.price, cartItem.linePrice)
        self.assertEqual(invoice.subtotal, Decimal(str(self.product1.price * 37.0 + self.product2.price * 2.0)))
        # self.assertEqual(invoice.tax, (self.product1.price * 37 + self.product2.price * 2) * 0.056)

