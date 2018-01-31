# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.views.decorators.cache import never_cache
from django.utils.translation import ugettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import (
    Campaign,
    SubscriptionPlugin,
    CampaignArchivePlugin,
    SelectedCampaignsPlugin
)
from .views import SubscriptionView
from .utils import get_subscription_plugin_form

@plugin_pool.register_plugin
class SubscriptionCMSPlugin(CMSPluginBase):
    cache = False
    render_template = 'aldryn_mailchimp/snippets/_subscription.html'
    module = _('MailChimp')
    name = _('Subscription Form')
    model = SubscriptionPlugin

    def render(self, context, instance, placeholder):
        request = context['request']
        context['form'] = get_subscription_plugin_form()(
            initial={'plugin_id': instance.pk,
                     'redirect_url': request.get_full_path()})
        return context

    def get_subscription_view(self):
        return SubscriptionView.as_view()

    def get_plugin_urls(self):
        subscription_view = self.get_subscription_view()

        return patterns('', url(
            r'^subscribe/$', never_cache(subscription_view),
            name='aldryn-mailchimp-subscribe'),
                        )


@plugin_pool.register_plugin
class CampaignArchive(CMSPluginBase):
    render_template = 'aldryn_mailchimp/plugins/campaign_archive.html'
    name = _('Campaign Archive')
    module = _('MailChimp')
    model = CampaignArchivePlugin

    def render(self, context, instance, placeholder):
        objects = Campaign.objects.published()
        if instance.categories.exists():
            objects = objects.filter(category__in=instance.categories.all())
        if instance.count:
            objects = objects[:instance.count]
        context['object_list'] = objects
        return context


@plugin_pool.register_plugin
class SelectedCampaigns(CMSPluginBase):
    render_template = 'aldryn_mailchimp/plugins/selected_campaigns.html'
    name = _('Selected Campaigns')
    module = _('MailChimp')
    model = SelectedCampaignsPlugin

    def render(self, context, instance, placeholder):
        context['object_list'] = instance.campaigns.all()
        return context
