from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User
from django.contrib.auth.forms import ValidationError
from django.core.validators import validate_email
from django.contrib.auth import password_validation, authenticate
from django.utils.translation import ugettext_lazy as _
import re
from django.contrib import messages

from ..utils import style_form


class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['first_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        input_type = 'text'
        style_form(self.fields, attrs={
            'class': 'form-control',
            'style': 'letter-spacing: 1px; color: #303030; font-weight:400',
        })

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            validate_email(email)
        except ValidationError as e:
            msg = 'Invalid Email Address.'
            self.add_error('password2', ValidationError(_(msg), code='invalid'))

        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        try:
            password_validation.validate_password(password1, user=User)
        except ValidationError as e:
            msg = 'Password is to short.'
            self.add_error('password1', ValidationError(_(msg), code='invalid'))
        return password1

    def clean_password2(self):
        if self.data['password2'] != self.data['password1']:
            msg = 'Passwords are not the same.'
            self.add_error('password2', ValidationError(_(msg), code='invalid'))


class LoginForm(AuthenticationForm):
    # email = forms.EmailField(label="Email Address", required=True)

    class Meta:
        model = User
        fields = ['password']

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        style_form(self.fields, attrs={
            'class': 'form-control',
            'style': 'letter-spacing: 1px; color: #303030; font-weight:400'
        })

    def clean(self):
        email = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        user = authenticate(email=email, password=password)
        if not user or not user.is_active:
            raise ValidationError("Invalid email or password.")

        return self.cleaned_data

    def login(self):
        email = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        user = authenticate(email=email, password=password)
        return user


class ForgotPasswordForm(forms.Form):
    email = forms.CharField(label='Email', widget=forms.TextInput(
        attrs={'class': 'form-control form-control-lg form-control-solid', 'type': 'email',
               'id': 'email', 'placeholder': _('Enter email')}))

    def clean_email(self):
        email = self.cleaned_data['email']

        try:
            validate_email(email)
        except ValidationError as e:
            raise forms.ValidationError(_('You have entered wrong email'))
        else:
            email_normalized = email.lower()  # fix case sensitive logging
            return email_normalized


class ResetPasswordForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(ResetPasswordForm, self).__init__(*args, **kwargs)
        style_form(self.fields, attrs={
            'class': 'form-control',
            'style': 'letter-spacing: 1px; color: #303030; font-weight:400'
        })

    password = forms.CharField(label=_('Password'), widget=forms.PasswordInput(
        attrs={'class': 'form-control form-control-lg form-control-solid',
               'id': 'userpassword', 'placeholder': _('Enter password')}))

    password_confirm = forms.CharField(label=_('Confirm password'), widget=forms.PasswordInput(
        attrs={'class': 'form-control form-control-lg form-control-solid',
               'id': 'conf_password', 'placeholder': _('Confirm password')}))

    def clean(self):
        try:
            password = self.cleaned_data['password']
            password_confirm = self.cleaned_data['password_confirm']
        except KeyError:
            raise forms.ValidationError(_('Please fill input fields'))

        if password != password_confirm:
            raise forms.ValidationError(_('Both password should be the same'))

        reg = "((?=.*\d)(?=.*[A-Za-z])(?=.*[/\!@#$%?=*&]).{8,100})"
        if not re.search(reg, password):
            raise forms.ValidationError(_('Password must be at least 8 character and contain symbols'))

        return self.cleaned_data


