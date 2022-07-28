from django.db import models
from ..account.models import User
from django.utils.translation import gettext_lazy as _


class Portfolio(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(_('Portfolio name'), max_length=255, unique=False, blank=True)
    total_cost = models.PositiveIntegerField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)

    class Meta:
        verbose_name = _('Portfolio')
        verbose_name_plural = _('Portfolios')

    def __str__(self):
        return self.name
