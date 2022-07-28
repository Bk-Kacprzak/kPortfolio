from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from .forms import PortfolioForm
from .models import Portfolio

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView


# TODO: delete it
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


class PortfolioCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    login_url = ('/auth/login')
    form_class = PortfolioForm
    template_name = "portfolio/portfolio.html"

    def get_form(self):
        form = super(PortfolioCreateView, self).get_form()
        return form

    def form_valid(self, form):
        portfolio = form.save(commit=False)
        portfolio.user = self.request.user
        portfolio.save()
        return redirect(reverse('portfolio_overview'))


class OverviewPanelView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    login_url = ('/auth/login')
    form_class = PortfolioForm
    template_name = "portfolio/overview.html"

    def get_context_data(self, **kwargs):
        # kwargs['portfolios'] = PortfolioForm.objects.filter(user=self.request.user)
        if 'portfolio_form' not in kwargs:
            kwargs['portfolio_form'] = PortfolioForm()
        # kwargs['asset_form'] = AssetForm
        return kwargs

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())

    def post(self, request, *args, **kwargs):
        context = {}
        if 'new_portfolio' in request.POST:
            form = PortfolioForm(request.POST)
            if form.is_valid():
                portfolio = form.save(commit=False)
                portfolio.user = request.user
                portfolio.save()
                return redirect(reverse('portfolio_overview'))
            else:
                form.add_error(None, "Form is invalid.")
                context['portfolio_form'] = form
                return render(request, self.template_name, self.get_context_data(**context))
        else:
            #TODO: CREATE TRANSACTION FORM HANDLER
            pass





# @login_required
# def portfolio_overview(request):
#     return render(request, "portfolio/overview.html", {})
