from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))

class BasketForm(forms.Form):
    post_id = forms.IntegerField(widget=forms.HiddenInput)
    number = forms.IntegerField(min_value=1,widget=forms.NumberInput(attrs={'class':'form-control'}), initial=1)