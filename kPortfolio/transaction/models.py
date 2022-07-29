from django.db import models
from ..asset.models import Asset
from ..portfolio.models import Portfolio
from django.utils.translation import gettext_lazy as _
from datetime import date


class TransactionManager(models.Manager):
    pass


class Transaction(models.Model):
    # id = models.AutoField(primary_key=True)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, null=False, blank=False)
    asset = models.ForeignKey(Asset, on_delete=models.PROTECT, null=False, blank=False)

    price = models.FloatField(_('Price'), null=False)
    cost = models.PositiveIntegerField(blank=True, null=True)
    amount = models.PositiveIntegerField(blank=True, null=True)
    date = models.DateField(_('Transaction date'), blank=True, null=True, default=date.today().strftime('%m/%d/%y'))

    type = models.CharField(_('Transaction type'), max_length=5

                            # choices=((u'1', _('buy')), (u'2', _('sell'))
                            , default='buy')

    objects = TransactionManager()

    class Meta:
        verbose_name = _('Transaction')
        verbose_name_plural = _('Transactions')

    def __str__(self):
        return f"{_('Transaction')} {self.id}"

    def get_transaction_types():
        return Transaction.type.choices
