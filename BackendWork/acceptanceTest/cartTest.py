# from django.test import TestCase
# from BackendWork.models import User, Product, Invoice
# from django.test import Client
# import json


# class accountManageTest(TestCase):
#     client = None
#     theList = None
#
#     def setUp(self):
#         self.client = Client()
#         self.userList = {"Mike": "Mike", "Bob": "Bob"}
#
#         for i in self.userList.keys():
#             temp = User(username=i, password=i)
#             temp.save()
#
#         self.productList = {"Computer": 25, "Science": 30, "Engineer": 45}
#
#         invoice = Invoice(invoiceId="1", customerId=User.objects.get(username="Bob").id)
#         invoice = Invoice(invoiceId="1", customerId=User.objects.get(username="Mike").id)
#
#         for i in self.productList.keys():
#             temp = Product(name=i, price=i)
#             temp.save()
