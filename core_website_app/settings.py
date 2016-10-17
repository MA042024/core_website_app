from django.conf import settings


MDCS_URI = getattr(settings, 'MDCS_URI', "http://localhost")
