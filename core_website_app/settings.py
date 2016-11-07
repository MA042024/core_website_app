from django.conf import settings

if not settings.configured:
    settings.configure()

MDCS_URI = getattr(settings, 'MDCS_URI', "http://localhost")

INSTALLED_APPS = (
    'core_main_app',
)
