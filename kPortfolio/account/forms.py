from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User
from django.contrib.auth.forms import ValidationError
from django.core.validators import validate_email
from django.contrib.auth import password_validation, authenticate
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages

class RegisterForm(UserCreationForm):
    # email = forms.EmailField(label="Email Address", required=True)

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
        user = authenticate(email = email, password = password)
        if not user or not user.is_active:
            raise ValidationError("Invalid email or password.")

        return self.cleaned_data

    def login(self) :
        email = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        print(email, password, flush = True)
        user = authenticate(email=email, password=password)
        return user


# class ForgotPasswordForm()

def style_form(fields, attrs):
    input_type = 'text'
    for field in fields.items():
        if "password" in field[0]:
            input_type = 'password'
        else:
            input_type = 'text'
        attrs['type'] = input_type
        field[1].widget = forms.TextInput(attrs=attrs)
