from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

@login_required
def portfolio(request):
    return render(request, "portfolio/portfolio.html", {})

def portfolio_overview(request):
    return render(request, "portfolio/overview.html", {})

