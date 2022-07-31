from ..external_api.coingecko.live_prices import get_coins_by_mc
from django.shortcuts import HttpResponse
from .models import Asset

from django.contrib.auth.decorators import user_passes_test

@user_passes_test(lambda u: u.is_superuser)
def load_asset_data(request):
    coins = get_coins_by_mc(1500)
    for coin in coins:
        if not Asset.objects.filter(name_id=coin['name_id']).exists():
            asset = Asset(
                name_id=coin['name_id'],
                name=coin['name'],
                ticker=coin['ticker'],
                image=coin['image'],
                price=coin['current_price'],
                market_cap=coin['market_cap'],
                market_cap_rank=coin['market_cap_rank'],
                total_volume=coin['total_volume'],
                high_24h=coin['high_24h'],
                low_24h=coin['low_24h'],
                price_change_24h=coin['price_change_24h'],
                price_change_percentage_24h=coin['price_change_percentage_24h'],
                circulating_supply=coin['circulating_supply'],
                total_supply=coin['total_supply'],
                max_supply=coin['max_supply'],
                ath=coin['ath']
            )
            asset.save()
    return HttpResponse("Assets added successfully!")

@user_passes_test(lambda u: u.is_superuser)
def update_asset_data(request):
    coins = get_coins_by_mc(1500)
    for coin in coins:
        try:
            Asset.objects.filter(name_id=coin['name_id']).update(
                price=coin['current_price'],
                market_cap=coin['market_cap'],
                market_cap_rank=coin['market_cap_rank'],
                total_volume=coin['total_volume'],
                price_change_24h=coin['price_change_24h']
            )

        except Asset.DoesNotExist:
            asset = Asset(
                name_id=coin['name_id'],
                name=coin['name'],
                ticker=coin['ticker'],
                image=coin['image'],
                price=coin['current_price'],
                market_cap=coin['market_cap'],
                market_cap_rank=coin['market_cap_rank'],
                total_volume=coin['total_volume'],
                high_24h=coin['high_24h'],
                low_24h=coin['low_24h'],
                price_change_24h=coin['price_change_24h'],
                price_change_percentage_24h=coin['price_change_percentage_24h'],
                circulating_supply=coin['circulating_supply'],
                total_supply=coin['total_supply'],
                max_supply=coin['max_supply'],
                ath=coin['ath']
            )
            asset.save()

    return HttpResponse("Assets updated successfully!")
# load_asset_data()

