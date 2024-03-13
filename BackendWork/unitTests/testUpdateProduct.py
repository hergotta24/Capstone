from django.test import TestCase, Client
from django.urls import reverse
from BackendWork.forms import AddProductForm
from BackendWork.models import User, Product, Storefront
import json


class UpdateProductViewTestCase(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create a storefront owned by the user
        self.storefront = Storefront.objects.create(owner=self.user, name='Test Store')

        # Create a product owned by the storefront
        self.product = Product.objects.create(
            soldByStoreId=self.storefront,
            name='Test Product',
            description='Description',
            price=9.99,
            qoh=99,
            weight=1.0,
            length=1.0,
            width=1.0,
            height=1.0
        )

        self.form_data = {
            'product_name': 'Updated Product Name',
            'price': 20.00,
            'description': 'Updated Description',
            'qoh': 50
        }

        # Create a client
        self.client = Client()

    def test_update_product_authenticated(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        response = self.client.post(f'/storefront/{self.product.productId}/',
                                    json.dumps(self.form_data), content_type="application/json", follow=True)
        self.assertEqual(response.status_code, 200)

        self.product.refresh_from_db()

        self.assertEqual(self.product.name, 'Updated Product Name')
        self.assertEqual(self.product.price, 20.00)
        self.assertEqual(self.product.description, 'Updated Description')
        self.assertEqual(self.product.qoh, 50)


    def test_update_product_wrong_owner(self):
        # Create another user
        another_user = User.objects.create_user(username='anotheruser', password='testpassword', email='test@gmail.com')

        # Log in the other user
        self.client.login(username='anotheruser', password='testpassword')

        # Prepare data for the POST request
        response = self.client.post(f'/storefront/{self.product.productId}/',
                                    json.dumps(self.form_data), content_type="application/json", follow=True)

        # Check if the response status code is 403 (forbidden)
        self.assertEqual(response.status_code, 403)
