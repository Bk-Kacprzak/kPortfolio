from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from .forms import PortfolioForm
from .models import Portfolio

@login_required
def portfolio(request):
    form = PortfolioForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            name = form.cleaned_data['name']
            total_cost = form.cleaned_data['total_cost']
            portfolio = form.save(commit=False)
            portfolio.user = request.user
            portfolio.save()
            return redirect(reverse('portfolio_overview'))

    return render(request, "portfolio/portfolio.html", {
        'form': form
    })


@login_required
def portfolio_overview(request):

    return render(request, "portfolio/overview.html", {})

