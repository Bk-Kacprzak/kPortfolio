from django.db import models
from ..portfolio.models import Portfolio
from django.utils.translation import gettext_lazy as _
import numpy as np


class AssetManager(models.Manager):
    def get_coins_names(self, amount):
        return self.filter(market_cap_rank__lte=amount)


class Asset(models.Model):
    name_id = models.CharField(_("Name id"), max_length=128, unique=True, db_index=True, null=False)
    name = models.CharField(_('Asset name'), max_length=50, unique=False, null=False, blank=True)
    ticker = models.CharField(_('Ticker'), max_length=6, unique=False, null=False)
    image = models.URLField(unique=False, null=True)
    price = models.FloatField(_('Price'), null=False)
    market_cap_rank = models.PositiveSmallIntegerField(_('Market cap rank'), null=True, unique=False, db_index=True)
    market_cap = models.BigIntegerField(_("Market Cap"), null=True, blank=True)
    total_volume = models.BigIntegerField(_("Total volume"), null=True, blank=True)
    high_24h = models.FloatField(_("High 24 h"), null=True, blank=True)
    low_24h = models.FloatField(_("Low 24 h"), null=True, blank=True)
    price_change_24h = models.FloatField(_("Price change 24h"), blank=True, null=True)
    price_change_percentage_24h = models.FloatField(_("Price change percentage 24h"), blank=True, null=True)
    circulating_supply = models.BigIntegerField(_("Circulating supply"), blank=True, null=True)
    total_supply = models.BigIntegerField(_("Total supply"), blank=True, null=True)
    max_supply = models.BigIntegerField(_("Max supply"), blank=True, null=True)
    ath = models.FloatField(_("All time high"), blank=True, null=True)

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


