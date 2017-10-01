# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool


class CampaignArchive(CMSApp):
    name = _('Campaign Archive')

    def get_urls(self, page=None, language=None, **kwargs):
        return['aldryn_mailchimp.urls']


apphook_pool.register(CampaignArchive)
