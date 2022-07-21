from django.contrib.auth import logout, authenticate, login
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.encoding import force_bytes, force_text
from django.conf import settings

from .models import User
from .forms import RegisterForm, LoginForm
from .decorators import user_not_logged_in
from .tokens import account_activation_token


@user_not_logged_in
def register_request(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            send_registration_email(request, user=user, email_to=form.cleaned_data.get('email'))
            return render(request, "account/auth/register-confirm.html")

    return render(request, "account/auth/register.html", {"form": form})


def email_confirmation(request):
    return render(request, "account/auth/login.html", {})


@user_not_logged_in
def forgot_request(request):
    return render(request, "account/auth/forgot.html", {})


def logout_request(request):
    logout(request)
    return HttpResponseRedirect('/account/login')


@user_not_logged_in
def login_request(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.login()
            if user:
                login(request, user)
                return redirect("/")
        else:
            messages.error(request, message="Invalid email address or password.")

    return render(request, "account/auth/login.html", {"login_form": form})


from django.utils.translation import gettext_lazy as _

from django.core.mail import send_mail


def send_registration_email(request, user, email_to):
    current_site = get_current_site(request)
    mail_subject = "Confirm Account Registration"
    email_subject = _('Activate your Account')
    message = render_to_string('account/auth/acc-active-account.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })

    text_content = 'This is an important message.'
    # message = render_to_string("account/auth/acc-active-account.html", {
    #     'user': user,
    #     'domain': current_site.domain,
    #     'uid':urlsafe_base64_encode(force_bytes(user.pk)),
    #     'token': account_activation_token.make_token(user)
    # })
    send_mail(
        email_subject, message,
        settings.EMAIL_HOST_USER,
        [email_to]
    )


def activate(request, uidb64, token):
    pass
