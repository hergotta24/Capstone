from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from BackendWork.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
from BackendWork.models import *


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
            return render(request, 'login.html', {'error': 'Invalid login credentials.'})


# accounts/views.py

class UserRegisterView(View):
    @staticmethod
    def get(request):
        user = request.user
        form = UserCreationForm(instance=user)
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
            'password2': password1,  # Assuming you want both password fields to have the same value
        }

        form = UserCreationForm(form_data)
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            return JsonResponse({'error': form.errors}, status=400)


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

        # Fetch the user instance you want to update
        user = User.objects.get(username=username)

        # Construct the form instance with the user instance and the updated data
        user.first_name = first_name
        user.last_name = last_name
        user.phone_number = phone_number

        user.save()

        return redirect('/')


def home(request):
    return render(request, 'home.html')


def customLogout(request):
    logout(request)
    return redirect('/')


def deleteProduct(request, productid):
    get_object_or_404(Product, id=productid)
    Product.objects.filter(productId=productid).delete()
    # return redirect('storefront/')
    # I assume it should redirect to the storefront, but my branch doesn't have that path


class ProductDeleteView(View):

    @staticmethod
    # @login_required(login_url='/login/')
    def post(request, productid):
        Product.objects.filter(productId=productid).delete()

