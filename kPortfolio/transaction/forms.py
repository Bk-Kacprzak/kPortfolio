import re

from .models import Transaction
from ..portfolio.models import Portfolio
from ..asset.models import Asset
from django import forms
import datetime

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ('price', 'cost', 'amount', 'date', 'type')
        attrs = {
            'class': 'form-control form-control-lg form-control-solid',
            'style': 'letter-spacing: 1px; color: #303030; font-weight:400'
        }
        widgets = {
            'price': forms.TextInput(attrs=attrs),
            'cost': forms.TextInput(attrs=attrs),
            'amount': forms.TextInput(attrs=attrs),
            'type': forms.TextInput(attrs=attrs),
            'date': forms.TextInput(attrs=attrs)
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(TransactionForm, self).__init__(*args, **kwargs)
        self.fields['portfolio_name'].queryset = Portfolio.objects.filter(user=self.user)

    portfolio_name = forms.ModelChoiceField(queryset=None, widget=forms.Select(attrs={'class': 'form-select '
                                                                                               'form-select-solid '
                                                                                               'form-select-lg '
                                                                                               'fw-bold'}),
                                            required=True)
    asset_name = forms.ModelChoiceField(queryset=Asset.objects.get_coins_names(5), widget=forms.Select(
        attrs={'class': 'form-select form-select-solid form-select-lg fw-bold'}))

    # date = forms.DateField(input_formats=['%m/%d/%y'], widget=forms.SelectDateWidget, initial=datetime.date.today())
    #
    # date = forms.DateTimeField(input_formats=('%d-%m-%y'),
    #                            widget=forms.SelectDateWidget(
    #                                attrs={'class': 'form-select '
    #                                                'form-select-solid '
    #                                                'form-select-lg '
    #                                                'fw-bold'}
    #                            ))
