# core_website_app

core_website_app is a Django app providing basic functionalities for a website.

## Quickstart

  1. Add "core_website_app" to your INSTALLED_APPS setting like this::

  ```python
  INSTALLED_APPS = [
      ...
      'core_website_app',
  ]
  ```

  2. Include the core_website_app URLconf in your project urls.py like this::

  ```python
  url(r'^website/', include('core_website_app.urls')),
  ```
