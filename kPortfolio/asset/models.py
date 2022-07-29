from django.db import models
from ..portfolio.models import Portfolio
from django.utils.translation import gettext_lazy as _


class AssetManager(models.Manager) :
    def get_coins_names(self, amount):
        return self.filter(marketcap__lte=amount)

class Asset(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(_('Asset name'), max_length=50, unique=False, null=False, blank=True)
    ticker = models.CharField(_('Ticker'), max_length=6, unique=False, null=False)

    price = models.FloatField(_('Price'), null=False)
    marketcap = models.PositiveSmallIntegerField(_('Market cap'), null=True, unique=True)

    # 24h change
    # 1w change
    # 1m change
    objects = AssetManager()

    def __str__(self):
        return self.name

    def get_price(self):
        return self.price

