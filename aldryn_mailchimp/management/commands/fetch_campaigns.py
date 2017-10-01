# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils.text import slugify
from django.utils.dateparse import parse_datetime

from mailchimp3 import MailChimp

from ...models import Campaign, Category


class Command(BaseCommand):

    keywords = None

    @staticmethod
    def fetch_keywords():
        keyword_groups = {
            'name': {},
            'subject': {},
            'listname': {},
            'content': {},
        }

        for category in Category.objects.filter(smart_match=True):
            for kw in category.keyword_set.all():
                if kw.scope_name:
                    keyword_groups['name'][kw.value.lower()] = kw.category.id
                if kw.scope_subject:
                    keyword_groups['subject'][kw.value.lower()] = kw.category.id
                if kw.scope_listname:
                    keyword_groups['listname'][kw.value.lower()] = kw.category.id
                if kw.scope_content:
                    keyword_groups['content'][kw.value.lower()] = kw.category.id
        return keyword_groups

    def search_category(self, campaign):
        attr_list = (
            # kw-group, campaign-attr
            ('name', 'mc_title'),
            ('subject', 'subject'),
            ('listname', 'list_name'),
            ('content', 'content_text'),
        )

        category_id = None

        for kw_group, campaign_attr in attr_list:
            if not category_id:
                for kw, cat in self.keywords[kw_group].items():
                    if getattr(campaign, campaign_attr) and \
                       kw in getattr(campaign, campaign_attr).lower():
                        category_id = cat
                        break

        return category_id

    def handle(self, *args, **options):
        self.keywords = self.fetch_keywords()
        mc = MailChimp(settings.MAILCHIMP_USERNAME, settings.MAILCHIMP_API_KEY)
        response = mc.campaigns.all(get_all=False)

        for each in response['campaigns']:
            campaign, created = Campaign.objects.get_or_create(cid=each['id'])
            campaign.send_time = parse_datetime(each['send_time'])
            campaign.mc_title = each['settings']['title']
            campaign.subject = each['settings']['subject_line']
            campaign.list_name = each['recipients']['list_name']
            campaign.list_id = each['recipients']['list_id']
            campaign.slug = slugify(each['settings']['subject_line'])[:50] \
                if each['settings']['subject_line'] else campaign.pk

            # content
            try:
                response_content = mc.campaigns.content.get(
                    campaign_id=campaign.cid)
            except Exception as e:
                print(e)
                campaign.hidden = True
            else:
                campaign.content_text = response_content['plain_text']
                campaign.content_html = response_content['archive_html']

            # match campaign to category (if not set yet)
            if not campaign.category:
                category_id = self.search_category(campaign)
                if category_id:
                    campaign.category = Category.objects.get(pk=category_id)

            campaign.save()

        print('Imported {0} campaigns'.format(response['total_items']))
