from django import forms
from django.contrib.auth.forms import UsernameField


class RegisterForm(forms.Form):
    username = UsernameField(max_length=32)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    password_confirm = forms.CharField(max_length=64)

    def is_valid(self):
        base_valid = super(RegisterForm, self).is_valid()
        password_are_same = self.data['password'] == self.data['password_confirm']
        return base_valid and password_are_same


class LoginForm(forms.Form):
    username = UsernameField(max_length=32)
    password = forms.CharField(max_length=64)
