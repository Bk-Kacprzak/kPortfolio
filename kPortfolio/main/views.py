from django.shortcuts import render
from django.views.generic import ListView
from django.core.paginator import Paginator
from ..asset.models import Asset

def index(request):
    coins = Asset.objects.filter(market_cap_rank__lte=1000).values(
        'market_cap_rank', 'image', 'name', 'price', 'market_cap', 'price_change_percentage_24h'
    )

    paginator = Paginator(coins, 100)
    page_number= request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
           }
    return render(request, "home/index.html", context)