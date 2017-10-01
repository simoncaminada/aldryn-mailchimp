# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _


class SubscriptionPluginForm(forms.Form):

    email = forms.EmailField(max_length=254, label=_('Email'))

    plugin_id = forms.CharField(widget=forms.HiddenInput)
    redirect_url = forms.CharField(widget=forms.HiddenInput)
