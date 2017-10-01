# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aldryn_mailchimp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='list_id',
            field=models.CharField(max_length=50, editable=False, blank=True, null=True, verbose_name='list id'),
        ),
        migrations.AddField(
            model_name='campaign',
            name='list_name',
            field=models.CharField(max_length=255, editable=False, blank=True, null=True, verbose_name='list name'),
        ),
        migrations.AddField(
            model_name='keyword',
            name='scope_listname',
            field=models.BooleanField(default=True, verbose_name='search in campaign list name'),
        ),
        migrations.AddField(
            model_name='subscriptionplugin',
            name='optin',
            field=models.BooleanField(help_text='If select perform double opt-in.', default=True, verbose_name='Double Opt-In'),
        ),
        migrations.AlterField(
            model_name='campaignarchiveplugin',
            name='categories',
            field=models.ManyToManyField(verbose_name='filter by category/categories', to='aldryn_mailchimp.Category'),
        ),
        migrations.AlterField(
            model_name='campaignarchiveplugin',
            name='cmsplugin_ptr',
            field=models.OneToOneField(to='cms.CMSPlugin', auto_created=True, primary_key=True, related_name='aldryn_mailchimp_campaignarchiveplugin', serialize=False, parent_link=True),
        ),
        migrations.AlterField(
            model_name='selectedcampaignsplugin',
            name='cmsplugin_ptr',
            field=models.OneToOneField(to='cms.CMSPlugin', auto_created=True, primary_key=True, related_name='aldryn_mailchimp_selectedcampaignsplugin', serialize=False, parent_link=True),
        ),
        migrations.AlterField(
            model_name='subscriptionplugin',
            name='cmsplugin_ptr',
            field=models.OneToOneField(to='cms.CMSPlugin', auto_created=True, primary_key=True, related_name='aldryn_mailchimp_subscriptionplugin', serialize=False, parent_link=True),
        ),
        migrations.AlterField(
            model_name='subscriptionplugin',
            name='list_id',
            field=models.CharField(help_text='ID of the list found in Mailchimp list: Settings > List name and defaults', max_length=20, verbose_name='List ID'),
        ),
    ]
