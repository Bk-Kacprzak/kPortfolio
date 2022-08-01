from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _
import re

from .models import Portfolio
from ..utils import style_form


class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ('name', 'total_cost')
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control form-control-lg form-control-solid',
                'style': 'letter-spacing: 1px; color: #303030; font-weight:400',
                'placeholder': _("Portfolio")
            }),
            'total_cost': forms.TextInput(attrs={
                'class': 'form-control form-control-lg form-control-solid',
                'style': 'letter-spacing: 1px; color: #303030; font-weight:400',
                'placeholder': _("Total Amount")
            }),
        }

    def __init__(self, *args, **kwargs):
        super(PortfolioForm, self).__init__(*args, **kwargs)
        # style_form(self.fields,  attrs={ 'class': 'form-control', 'style': 'letter-spacing: 1px; width: 340px;
        # background: white; height: 40px; color: #303030; font-weight:400', })


