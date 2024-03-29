from django.test import TestCase

from BackendWork.models import User, Storefront, Product


class TestFavorites(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='testUser', password='p@55w0rD', email='testuser@gmail.com')
        self.user2 = User.objects.create_user(username='testUser2', password='p@55w0rD', email='testuser2@gmail.com')
        self.storefront1 = Storefront.objects.create(owner=self.user1, name='Test Storefront')
        self.product1 = Product.objects.create(soldByStoreId=self.storefront1, name='Test Product',
                                               description='Description', price=9.99, qoh=99, weight=1.0, length=1.0,
                                               width=1.0, height=1.0)
        self.product2 = Product.objects.create(soldByStoreId=self.storefront1, name='Test Product2',
                                               description='Description', price=9.99, qoh=99, weight=1.0, length=1.0,
                                               width=1.0, height=1.0)

    def testNoFavorites(self):
        self.assertFalse(self.user1.has_favorite(self.product1), "product1 should not have been favorited "
                                                                 "by user1")

    def testAddRemoveFavorites(self):
        self.user1.add_favorite(self.product1)
        self.assertTrue(self.user1.has_favorite(self.product1), "product1 should have been favorited by user1")
        self.assertFalse(self.user1.has_favorite(self.product2), "product2 should not have been favorited "
                                                                 "by user1")

        self.user1.remove_favorite(self.product1)
        self.assertFalse(self.user1.has_favorite(self.product1), "product1 should no longer be favorited "
                                                                 "by user1")
        self.assertFalse(self.user1.has_favorite(self.product2), "product2 should not be favorited "
                                                                 "by user1")

    def testMultipleProducts(self):
        self.user1.add_favorite(self.product1)
        self.user1.add_favorite(self.product2)
        self.assertTrue(self.user1.has_favorite(self.product1), "product1 should have been favorited by user1")
        self.assertTrue(self.user1.has_favorite(self.product2), "product2 should have been favorited by user1")
        self.assertIn(self.product1, self.user1.get_favorites(), "product1 should be in user1's favorites list")
        self.assertIn(self.product2, self.user1.get_favorites(), "product1 should be in user1's favorites list")

        self.user1.remove_favorite(self.product1)
        self.assertFalse(self.user1.has_favorite(self.product1), "product1 should no longer be favorited "
                                                                 "by user1")
        self.assertTrue(self.user1.has_favorite(self.product2), "product2 should still be favorited "
                                                                "by user1")
        self.assertNotIn(self.product1, self.user1.get_favorites(), "product1 should no longer be in user1's "
                                                                    "favorites list")
        self.assertIn(self.product2, self.user1.get_favorites(), "product2 should still be in user1's favorites list")

        self.user1.remove_favorite(self.product2)
        self.assertFalse(self.user1.has_favorite(self.product1), "product1 should no longer be favorited "
                                                                 "by user1")
        self.assertFalse(self.user1.has_favorite(self.product2), "product2 should no longer be favorited "
                                                                 "by user1")
        self.assertNotIn(self.product1, self.user1.get_favorites(), "product1 should no longer be in user1's "
                                                                    "favorites list")
        self.assertNotIn(self.product2, self.user1.get_favorites(), "product2 should no longer be in user1's "
                                                                    "favorites list")

    def testMultipleUsers(self):
        self.user1.add_favorite(self.product1)
        self.user2.add_favorite(self.product1)
        self.assertTrue(self.user1.has_favorite(self.product1), "product1 should have been favorited by user1")
        self.assertTrue(self.user2.has_favorite(self.product1), "product1 should have been favorited by user2")

        self.user1.remove_favorite(self.product1)
        self.assertFalse(self.user1.has_favorite(self.product1), "product1 should no longer be favorited by user1")
        self.assertTrue(self.user2.has_favorite(self.product1), "product1 should have been favorited by user2")

        self.user2.remove_favorite(self.product1)
        self.assertFalse(self.user1.has_favorite(self.product1), "product1 should no longer be favorited by user1")
        self.assertFalse(self.user2.has_favorite(self.product1), "product1 should no longer be favorited by user2")
