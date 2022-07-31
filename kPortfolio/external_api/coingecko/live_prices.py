import requests
from pycoingecko import CoinGeckoAPI
import math

cg = CoinGeckoAPI()


def get_coins_by_mc(amount=1):
    MAX_AMOUNT = 250 #max number of coins to get per request
    pages = math.ceil(amount / MAX_AMOUNT)
    amount_left = amount
    data = []
    for page in range(pages):
        _amount = MAX_AMOUNT if page + 1 != pages else amount_left % amount
        amount_left -= _amount
        print(page)
        coins = serialize_data(
            cg.get_coins_markets(vs_currency='usd', order='market_cap_desc', page=page, per_page=_amount))
        for coin in coins:
            data.append(coin)
    return data


def serialize_data(coins):
    data = []
    for coin in coins:
        data.append({
            'name_id': coin['id'],
            'name': coin['name'],
            'ticker': coin['symbol'],
            'image': coin['image'],
            'current_price': coin['current_price'],
            'market_cap': coin['market_cap'],
            'market_cap_rank': coin['market_cap_rank'],
            'total_volume': coin['total_volume'],
            'high_24h': coin['high_24h'],
            'low_24h': coin['low_24h'],
            'price_change_24h': coin['price_change_24h'],
            'price_change_percentage_24h': coin['price_change_percentage_24h'],
            'circulating_supply': coin['circulating_supply'],
            'total_supply': coin['total_supply'],
            'max_supply': coin['max_supply'],
            'ath': coin['ath']
        })

    return data
