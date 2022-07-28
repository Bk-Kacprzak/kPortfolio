from django.db import models
from ..asset.models import Asset
from ..portfolio.models import Portfolio
from django.utils.translation import gettext_lazy as _


class Transaction(models.Model):
    id = models.AutoField(primary_key=True)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, null=False, blank=False)
    asset = models.ForeignKey(Asset, on_delete=models.PROTECT, null=False, blank=False)

    price = models.FloatField(_('Price'), null=False)
    total_cost = models.PositiveIntegerField(blank=True, null=True)
    notes = models.CharField(max_length=512, blank=True, null=True)

    class Meta:
        verbose_name = _('Portfolio')
        verbose_name_plural = _('Portfolios')

    def __str__(self):
        return f"{_('Transaction')} {self.id}"
