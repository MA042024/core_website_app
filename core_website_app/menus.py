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
