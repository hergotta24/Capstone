from django.test import TestCase, Client
import json
from BackendWork.forms import UserCreationForm
from BackendWork.models import User


class RegistrationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.form_data = {
            'email': 'test@uwm.edu',
            'username': 'testAccount',
            'password1': 'p@55w0rD!',
            'password2': 'p@55w0rD!',
            # 'first_name': 'Test',
            # 'last_name': 'Account',
            # 'phone_number': '1234567890',
            # 'shipping_address': '123 Fake St.',  # will need to be changed to Address model
            # 'billing_address': '123 Fake St.',  # will need to be changed to Address model
        }

    def testRegistrationPageAccessible(self):  # might technically be an acceptance test?
        response = self.client.get('/register/')
        self.assertEqual(response.status_code, 200, "registration page not returning 200 OK")

    def testRegistrationSuccessRedirect(self):  # might technically be an acceptance test?
        # response = self.client.post('/register/', self.form_data, follow=True)
        response = self.client.post('/register/', json.dumps(self.form_data), content_type="application/json",
                                    follow=True)
        self.assertEqual(response.status_code, 200, "registration page not returning 200 OK upon successful"
                                                    " registration")

    def testRegistrationFormValid(self):
        form = UserCreationForm(data=self.form_data)
        self.assertTrue(form.is_valid(), "valid form data returned false")

    def testRegistrationDuplicateEmail(self):
        User.objects.create_user(username='alreadyExists', email='already@exists.com', password='p@55w0rD!',
                                 first_name='Already', last_name='Exists', phone_number='1234567890')
        self.form_data['email'] = 'already@exists.com'
        form = UserCreationForm(data=self.form_data)
        self.assertFalse(form.is_valid(), "account already exists with this email")
        self.assertIn('email', form.errors, "email field not found in form.errors")

    def testRegistrationDuplicateUsername(self):
        User.objects.create_user(username='alreadyExists', email='already@exists.com', password='p@55w0rD!',
                                 first_name='Already', last_name='Exists', phone_number='1234567890')
        self.form_data['username'] = 'alreadyExists'
        form = UserCreationForm(data=self.form_data)
        self.assertFalse(form.is_valid(), "account already exists with this username")
        self.assertIn('username', form.errors, "username field not found in form.errors")

    def testRegistrationFormInvalidEmail(self):
        self.form_data['email'] = ''
        form = UserCreationForm(data=self.form_data)
        self.assertFalse(form.is_valid(), "form data missing email")

        self.form_data['email'] = 'invalidEmail'
        form = UserCreationForm(data=self.form_data)
        self.assertFalse(form.is_valid(), "form data has invalid email address")

    def testRegistrationFormInvalidUsername(self):
        self.form_data['username'] = ''
        form = UserCreationForm(data=self.form_data)
        self.assertFalse(form.is_valid(), "form data missing username")

    def testRegistrationPasswordMismatch(self):
        self.form_data['password2'] = 'mismatch'
        form = UserCreationForm(data=self.form_data)
        self.assertFalse(form.is_valid(), "form data has mismatched passwords")

    # def testRegistrationFormInvalidFirstname(self):
    #     self.form_data['first_name'] = ''
    #     form = UserCreationForm(data=self.form_data)
    #     self.assertFalse(form.is_valid(), "form data missing first_name")
    #
    # def testRegistrationFormInvalidLastname(self):
    #     self.form_data['last_name'] = ''
    #     form = UserCreationForm(data=self.form_data)
    #     self.assertFalse(form.is_valid(), "form data missing last_name")
    #
    # def testRegistrationFormInvalidPhone(self):
    #     self.form_data['phone_number'] = ''
    #     form = UserCreationForm(data=self.form_data)
    #     self.assertFalse(form.is_valid(), "form data missing phone_number")
    #
    # def testRegistrationFormInvalidShipping(self):
    #     self.form_data['shipping_address'] = ''
    #     form = UserCreationForm(data=self.form_data)
    #     self.assertFalse(form.is_valid(), "form data missing shipping_address")
    #
    # def testRegistrationFormInvalidBilling(self):
    #     self.form_data['billing_address'] = ''
    #     form = UserCreationForm(data=self.form_data)
    #     self.assertFalse(form.is_valid(), "form data missing billing_address")
