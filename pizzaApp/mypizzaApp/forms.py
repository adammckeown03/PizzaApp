from django import forms
from . import models
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import transaction
from .models import User


class UserSignupForm(UserCreationForm):
    email = forms.EmailField(label="Email")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['email', 'password1', 'password2']

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_admin = False
        
        if commit:
            user.save()
        
        return user


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

class PizzaForm(forms.ModelForm):
    class Meta:
        model = models.Pizza
        fields = ['size', 'crust', 'sauce', 'cheese', 'toppings']
    
    toppings = forms.ModelMultipleChoiceField(
        queryset=models.Topping.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

class OrderForm(forms.ModelForm):
    class Meta:
        model = models.Order
        fields = ['name', 'address', 'card_number', 'expiry_month', 'expiry_year', 'cvv']