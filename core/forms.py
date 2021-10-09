from django.contrib.auth.forms import UserCreationForm
from django.db import models
from django.forms import fields
from django.shortcuts import render
from django import forms
from django.contrib.auth import get_user_model
from order.models import *
User = get_user_model()

class CreateUSerForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['first_name','last_name','street_address','apartment_address','country','city','phone_number']

class PaymentMethodForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['payment_method']