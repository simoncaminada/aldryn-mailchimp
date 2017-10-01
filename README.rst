################
Aldryn MailChimp
################

Aldryn MailChimp is the easiest way to integrate MailChimp into
`Aldryn <http://aldryn.com>`_ and `django CMS <http://django-cms.org/>`_ sites.

With Aldryn MailChimp you can:

- Allow users to subscribe to mailing lists (CMS Plugin)
- Displays existing campaigns (App Hook + CMS Plugins)

To activate MailChimp integration:

- provide an Mailchimp ``User Name`` and ``API Key`` while installing the Aldryn app
- add the Mailchimp subscription form to your CMS page placeholder
- create an CMS page for hooking the app for displaying existing campaigns (optional)

Notice:
Grab `API Key` from your mailchimp account (Account > Extra > Api Keys). And
`User Name` is the one you use to login on the website and is optional.

===========
CMS Plugins
===========

- Submission (form with email field form)

=============
App Hook Page
=============

- Campaign Archives (List campaign archives)
- Selected Campaign (Show html or text of selected campaign)

++++++++++++
Get Campaign
++++++++++++

Use the Django management command ``fetch_campaigns`` to retrieve current campaigns::

  $ python manage.py fetch_campaigns

Notice: this command can be run from admin Campaign view action list.

===============================
Categories + Automatic Matching
===============================

Version 0.2.4 introduced categories with automatic matching. You can define
categories and add keywords to those categories to automatically sort synced
campaigns into categories. You can define priorities for both campaigns and
their keywords. Used in app hook page.

++++++++
Matching
++++++++

Once the campaigns have been fetched, the automatic matcher will go through all
categories (starting from the top as defined in
``/admin/aldryn_mailchimp/category/``) and scan each campaign for the defined
keywords. You can specify keywords to be searched in any or multiple of the
following three:

- campaign title
- campaign subject
- campaign content
- campaign list name

Once a match is found, the search for the current campaign will be stopped, the
found category will be assigned to the campaign and the matcher will then
continue with the next campaign.

=========
Changelog
=========

- Base version: 0.3.0
- Migrated to Python 3.5, plus switch to the Python Mailchimp v3.0 client API
- django-CMS 3.3+ compatible
