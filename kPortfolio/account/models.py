from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):
        if not email :
            raise ValueError("Email is required.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password=None, **extra_fields):
        if not validate_is_none(username, email):
            return

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        if not validate_is_none(password):
            return

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    username = None
    first_name = models.CharField(_('first name'), max_length=255, unique=False, db_index=True)
    email = models.EmailField(_('email address'), unique=True, db_index=True)
    email_activated = models.BooleanField(default=False, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    is_staff = True

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email


def validate_is_none(*args):
    for value in args:
        if value is None:
            raise ValidationError(f'{value} is required.')

    return True
