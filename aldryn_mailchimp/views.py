# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.utils.translation import ugettext, ugettext_lazy as _
from django.views.generic import FormView, DetailView

from mailchimp3 import MailChimp

from .utils import get_language_for_code
from .forms import SubscriptionPluginForm
from .models import SubscriptionPlugin, Campaign


ERROR_MESSAGES = {
    500: ugettext('Oops, something must have gone wrong. Please try again later.'),
    401: ugettext('Invalid Mailchimp Username or API-Key.'),
    404: ugettext('The selected list does not exist.'),
    200: ugettext('You are already subscribed to our list.'),
    201: ugettext('You have successfully subscribed to our mailing list.'),
}


class SubscriptionView(FormView):
    form_class = SubscriptionPluginForm
    template_name = 'aldryn_mailchimp/subscription.html'

    def form_valid(self, form):
        mclient = MailChimp(
            settings.MAILCHIMP_USERNAME, settings.MAILCHIMP_API_KEY)

        plugin = get_object_or_404(
            SubscriptionPlugin, pk=form.cleaned_data['plugin_id'])

        # check if list exist or Username/API KEY wrong
        try:
            mclient.lists.get(list_id=plugin.list_id)
        except Exception as err:
            try:
                message = ERROR_MESSAGES[err.response.status_code]
            except (AttributeError, KeyError):
                message = ERROR_MESSAGES[500]

            if self.request.user.is_superuser and err:
                message = ugettext('{0} ({1})').format(message, err)

            messages.error(self.request, message)
            return redirect(form.cleaned_data['redirect_url'])

        # set double opt-in or not
        optin = 'subscribed'
        if plugin.optin:
            optin = 'pending'

        data = {
            'email_address': form.cleaned_data['email'],
            'status': optin
        }

        if plugin.assign_language:
            language = get_language_for_code(self.request.LANGUAGE_CODE)
            if language:
                data.update({'language': language})

        # add member to list
        try:
            mclient.lists.members.create(plugin.list_id, data)
        except Exception as err:
            json_err = err.response.json()
            message = ERROR_MESSAGES[500]
            if err.response.status_code == 400:
                if json_err.get('title') == 'Member Exists':
                    message = ERROR_MESSAGES[200]

            if self.request.user.is_superuser and json_err:
                message = ugettext('{0} ({1})').format(
                    message,
                    json_err.get('detail'))

            messages.error(self.request, message)
        else:
            messages.success(self.request, ugettext(ERROR_MESSAGES[201]))
        return redirect(form.cleaned_data['redirect_url'])

    def form_invalid(self, form):
        redirect_url = form.data.get('redirect_url')

        if redirect_url:
            message = _('Please enter a valid email.')

            messages.error(self.request, message)
            response = HttpResponseRedirect(redirect_url)
        else:
            # user has tampered with the redirect_url field.
            response = HttpResponseBadRequest()
        return response


class CampaignDetail(DetailView):
    model = Campaign

    @property
    def template_name_suffix(self):
        default = '_detail'
        iframe = '_detail_iframe'
        return iframe if 'iframe' in self.request.GET else default

    def get_queryset(self):
        return self.model.objects.published()


campaign_detail = CampaignDetail.as_view()
