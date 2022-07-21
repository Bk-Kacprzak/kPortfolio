from django.contrib.auth import logout, authenticate, login
from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponseRedirect
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.encoding import force_bytes, force_text
from django.conf import settings

from .models import User
from .forms import RegisterForm, LoginForm, ForgotPasswordForm, ResetPasswordForm
from .decorators import user_not_logged_in
from .tokens import generate_token

from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required


@user_not_logged_in
def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            send_registration_email(request, user=user, email_to=form.cleaned_data.get('email'))
            return render(request, "account/auth/register-confirm.html")

    return render(request, "account/auth/register.html", {"form": form})


@user_not_logged_in
def login_request(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.login()
            if not user.email_activated:
                return render(request, 'account/auth/verify-email.html')
            if user:
                login(request, user)
                return redirect("/")
        else:
            messages.error(request, _("Invalid email address or password."))

    return render(request, "account/auth/login.html", {"login_form": form})


@user_not_logged_in
def forgot_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.filter(email=email).first()
            if not user.email_activated:
                return render(request, 'account/auth/verify-email.html')
            if user:
                email_send = send_forgot_password_mail(request, user)
                messages.success(request, _('Check out your e-mail account. We have sent reset password mail.'))
            else:
                messages.error(request, _('This e-mail does not exist in our service.'))
    else:
        form = ForgotPasswordForm()

    return render(request, "account/auth/forgot-password.html", {
        'form': form
    })


def send_registration_email(request, user, email_to):
    current_site = get_current_site(request)
    mail_subject = "Confirm Account Registration"
    email_subject = _('Activate your Account')
    message = render_to_string('account/auth/acc-active-account.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_token.make_token(user),
    })

    text_content = 'This is an important message.'
    msg = EmailMultiAlternatives(email_subject, text_content, settings.DEFAULT_EMAIL_SENDER, [user.email])
    msg.attach_alternative(message, "text/html")

    return msg.send()


def send_forgot_password_mail(request, user):
    current_site = get_current_site(request)
    email_subject = _('Change your Password')
    message = render_to_string('account/auth/forgot-password-mail.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_token.make_token(user),
    })

    text_content = 'This is an important message.'
    msg = EmailMultiAlternatives(email_subject, text_content, settings.DEFAULT_FROM_EMAIL, [user.email])
    msg.attach_alternative(message, "text/html")
    return msg.send()


def activate(request, uidb64, token):
    uid = force_str(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=uid)

    if user is not None and generate_token.check_token(user, token):
        user.email_activated = True
        user.save()
        return redirect('login')

    return redirect(reverse('index')) #TODO: create template if activation refused


@user_not_logged_in
def reset_password(request, uidb64, token):
    uid = force_str(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=uid)

    form = ResetPasswordForm()
    if not user.email_activated:
        return render(request, 'account/auth/verify-email.html')

    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if not form.is_valid():
            return render(request, "account/auth/reset-password.html", {
                'form': form
            })

        password = form.cleaned_data['password']
        if generate_token.check_token(user, token):
            user.set_password(password)
            user.save()
            return redirect(reverse('login'))
        else:
            messages.error(request, _('Your token has expired'))

    return render(request, "account/auth/reset-password.html", {
        'form': form
    })


def logout_request(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect(reverse('index'))
