from django.core.urlresolvers import reverse
from menu import Menu, MenuItem


Menu.add_item(
    "main", MenuItem("Home", reverse("core_website_homepage"), icon="fa-home")
)

Menu.add_item(
    "main", MenuItem("Contact", reverse("core_website_contact"))
)

Menu.add_item(
    "main", MenuItem("Help", reverse("core_website_help"))
)

Menu.add_item(
    "footer", MenuItem("Privacy policy", reverse("core_website_privacy"))
)

Menu.add_item(
    "footer", MenuItem("Terms of use", reverse("core_website_terms"))
)

website_children = (
    MenuItem("Privacy Policy", reverse("admin:core_website_app_privacy"), icon="user-secret"),
    MenuItem("Terms of Use", reverse("admin:core_website_app_terms"), icon="file-text-o"),
    MenuItem("Help Page", reverse("admin:core_website_app_help"), icon="question-circle-o"),
)

Menu.add_item(
    "admin", MenuItem("WEBSITE", None, children=website_children)
)
