from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Item, Category

class UserRegisterationForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ItemForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(),initial=0)
    class Meta:
        model = Item
        fields = ['name', 'quantity', 'category']