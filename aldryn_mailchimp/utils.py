# -*- coding: utf-8 -*-

from django.conf import settings

try:
    import importlib
except ImportError:
    # python 2.6 compatibility
    from django.utils import importlib


def get_callable(string_or_callable):
    """
    If given a callable then it returns it, otherwise it resolves the path
    and returns an object.
    """
    if callable(string_or_callable):
        return string_or_callable
    else:
        module_name, object_name = string_or_callable.rsplit('.', 1)
        module = importlib.import_module(module_name)
        return getattr(module, object_name)


def get_subscription_plugin_form():
    if settings.MAILCHIMP_SUBSCRIPTION_PLUGIN_FORM:
        return get_callable(settings.MAILCHIMP_SUBSCRIPTION_PLUGIN_FORM)
    else:
        from .forms import SubscriptionPluginForm
        return SubscriptionPluginForm


# http://kb.mailchimp.com/article/can-i-see-what-languages-my-subscribers-use#code
MAILCHIMP_LANGUAGES = [
    'en', 'ar', 'af', 'be', 'bg', 'ca', 'zh', 'hr', 'cs', 'da', 'nl', 'et',
    'fa', 'fi', 'fr', 'fr_CA', 'de', 'el', 'he', 'hi', 'hu', 'is', 'id', 'ga',
    'it', 'ja', 'km', 'ko', 'lv', 'lt', 'mt', 'ms', 'mk', 'no', 'pl', 'pt',
    'pt_PT', 'ro', 'ru', 'sr', 'sk', 'sl', 'es', 'es_ES', 'sw', 'sv', 'ta',
    'th', 'tr', 'uk', 'vi',
]


def get_language_for_code(code):
    if code in MAILCHIMP_LANGUAGES:
        return code
    if code[:2] in MAILCHIMP_LANGUAGES:
        return code[:2]
    return None
