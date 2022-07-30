from django.db import models
from ..portfolio.models import Portfolio
from django.utils.translation import gettext_lazy as _
import numpy as np


class AssetManager(models.Manager):
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


class UserAsset(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, null=False, blank=False)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, null=False)

    average_buy_price = models.FloatField(_('Average buy'), blank=True, default=0, editable=True)
    average_sell_price = models.FloatField(_('Average sell'), blank=True, default=0, editable=True)

    amount = models.FloatField(_('Total amount'), blank=True, default=0, editable=True)
    max_amount = models.FloatField(_('Max amount'), blank=True, default=0, editable=True)


    def __str__(self):
        return f"Asset name: {self.asset.name}; User:{self.portfolio.user}; Portfolio:{self.portfolio}"

    def get_info(self):
        return f"{_('Amount')}: {self.amount}" \
               f"{_('Max amount')}: {self.max_amount}" \
               f"{_('Average buy price')}: {self.average_buy_price} " \
               f"{_('Average sell price')}: {self.average_sell_price} " \


    def get_transactions(self):
        return self.transaction_set.filter(portfolio=self.portfolio)

    def count_values(self, transaction):
        count = 1 if transaction['type'] == 'buy' else -1
        if transaction['type'] == 'buy':
            self.average_buy_price = np.average(a=[self.average_buy_price, transaction['price']],
                                                weights=[self.amount, transaction['amount']])
        else:
            self.average_sell_price = np.average(a=[self.average_sell_price, transaction['price']],
                                                weights=[self.max_amount-self.amount, transaction['amount']])
        self.amount += transaction['amount'] * count
        if self.amount > self.max_amount:
            self.max_amount = self.amount


