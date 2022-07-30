from django.shortcuts import render, redirect, get_object_or_404, reverse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView
from django.conf import settings

from .forms import PortfolioForm
from .models import Portfolio
from ..transaction.forms import TransactionForm
from ..asset.models import Asset, UserAsset


class PortfolioCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    login_url = settings.LOGIN_URL
    form_class = PortfolioForm
    template_name = "portfolio/portfolio.html"

    def get(self, request):
        if self.request.user.get_portfolios():
            return redirect(reverse('portfolio_overview'))

        return super(PortfolioCreateView, self).get(request)

    def get_form(self):
        form = super(PortfolioCreateView, self).get_form()
        return form

    def form_valid(self, form):
        if Portfolio.objects.filter(user=self.request.user, name=form.cleaned_data['name']).exists():
            return HttpResponse("User has portoflio with this name.")
        portfolio = form.save(commit=False)
        portfolio.user = self.request.user
        portfolio.save()
        return redirect(reverse('portfolio_overview'))


class OverviewPanelView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    login_url = settings.LOGIN_URL
    form_class = PortfolioForm
    template_name = "portfolio/overview.html"

    def get_context_data(self, **kwargs):
        # kwargs['portfolios'] = PortfolioForm.objects.filter(user=self.request.user)
        kwargs['portfolios'] = self.request.user.get_portfolios()
        if 'portfolio_form' not in kwargs:
            kwargs['portfolio_form'] = PortfolioForm()
        if 'transaction_form' not in kwargs:
            kwargs['transaction_form'] = TransactionForm(user=self.request.user)

        return kwargs

    def get(self, request, *args, **kwargs):
        if self.request.user.get_portfolios():
            return render(request, self.template_name, self.get_context_data())

        return redirect(reverse('portfolio'))


def post(self, request, *args, **kwargs):
        context = {}
        if 'new_portfolio' in request.POST:
            form = PortfolioForm(request.POST)
            if form.is_valid():
                if Portfolio.objects.filter(user=request.user, name=form.cleaned_data['name']).exists():
                    return HttpResponse("User has portoflio with this name.")
                portfolio = form.save(commit=False)
                portfolio.user = request.user
                portfolio.save()
                return redirect(reverse('portfolio_overview'))
            else:
                form.add_error(None, "Form is invalid.")
                context['portfolio_form'] = form
                return render(request, self.template_name, self.get_context_data(**context))
        elif 'new_transaction' in request.POST:
            form = TransactionForm(request.POST, user=request.user)
            if form.is_valid():
                transaction = form.save(commit=False)
                transaction.portfolio = Portfolio.objects.get(user=request.user,
                                                              name=form.cleaned_data['portfolio_name'])
                asset = None
                try:
                    asset = UserAsset.objects.get(portfolio=transaction.portfolio,
                                                  asset=form.cleaned_data['asset_name'])

                except UserAsset.DoesNotExist:
                    if transaction.type == 'buy':
                        asset = UserAsset(asset=Asset.objects.get(name=form.cleaned_data['asset_name']),
                                          portfolio=transaction.portfolio)
                    else:
                        form.add_error(None, "Cannot do sell transaction to an asset that does not exist.")
                        context['transaction_form'] = form
                        return render(request, self.template_name, self.get_context_data(**context))

                asset.count_values({
                    'cost': transaction.cost,
                    'price': transaction.price,
                    'amount': transaction.amount,
                    'type': transaction.type
                })
                asset.save()
                transaction.asset = asset
                # transaction.asset = Asset.objects.get(name=form.cleaned_data['asset_name'])
                transaction.save()
                return HttpResponse(transaction.portfolio.get_transactions())
            else:
                form.add_error(None, "Form is invalid.")
                print(form.errors)
                context['transaction_form'] = form
                return render(request, self.template_name, self.get_context_data(**context))


@login_required
def portfolio(request):
    form = PortfolioForm()
    if request.method == "POST":
        form = PortfolioForm(request.POST)
        if form.is_valid():
            portfolio = form.save(commit=False)
            portfolio.user = request.user
            portfolio.save()
            return redirect(reverse('portfolio_overview'))

    return render(request, "portfolio/overview.html", {'portfolio_form': form})
