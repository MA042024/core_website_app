from django.conf import settings

if not settings.configured:
    settings.configure()

SERVER_URI = getattr(settings, "SERVER_URI", "http://localhost")

INSTALLED_APPS = ("core_main_app",)

DISPLAY_NIST_HEADERS = getattr(settings, "DISPLAY_NIST_HEADERS", False)
""" boolean: display the NIST header
"""
DISPLAY_PRIVACY_POLICY_FOOTER = getattr(
    settings, "DISPLAY_PRIVACY_POLICY_FOOTER", False
)
""" boolean: display the privacy policy link in the footer
"""
DISPLAY_TERMS_OF_USE_FOOTER = getattr(settings, "DISPLAY_TERMS_OF_USE_FOOTER", False)
""" boolean: display the terms of use link in the footer
"""
DISPLAY_CONTACT_FOOTER = getattr(settings, "DISPLAY_CONTACT_FOOTER", False)
""" boolean: display the contact link in the footer
"""
DISPLAY_HELP_FOOTER = getattr(settings, "DISPLAY_HELP_FOOTER", False)
""" boolean: display the help link in the footer
"""
DISPLAY_RULES_OF_BEHAVIOR_FOOTER = getattr(
    settings, "DISPLAY_RULES_OF_BEHAVIOR_FOOTER", False
)
""" boolean: display the rules of behavior link in the footer
"""
SEND_EMAIL_WHEN_ACCOUNT_REQUEST_IS_ACCEPTED = getattr(
    settings, "SEND_EMAIL_WHEN_ACCOUNT_REQUEST_IS_ACCEPTED", False
)
""" boolean: send an email when an account is accepted
"""
SEND_EMAIL_WHEN_ACCOUNT_REQUEST_IS_DENIED = getattr(
    settings, "SEND_EMAIL_WHEN_ACCOUNT_REQUEST_IS_DENIED", False
)
""" boolean: send an email when an account is denied
"""
