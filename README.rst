=====
core_website_app
=====

core_website_app is a Django app. For each

Quick start
-----------

1. Add "core_website_app" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'core_website_app',
    ]

2. Include the polls URLconf in your project urls.py like this::

    url(r'^website/', include('core_website_app.urls')),

