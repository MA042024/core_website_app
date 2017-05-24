"""
    Admin views
"""
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from core_main_app.utils.rendering import admin_render as render
from core_website_app.views.admin.forms import TextAreaForm
from core_website_app.components.web_page.models import WebPage, WEB_PAGE_TYPES
import core_website_app.components.account_request.api as account_request_api
import core_website_app.components.contact_message.api as contact_message_api
import core_website_app.components.help.api as help_api
import core_website_app.components.privacy_policy.api as privacy_policy_api
import core_website_app.components.terms_of_use.api as terms_of_use_api
from django.views.generic import View


@staff_member_required
def user_requests(request):
    """ Page that allows to accept or deny user requests

        Args:
            request:

        Returns:
    """
    # Call the API
    requests = account_request_api.get_all()

    assets = {
        "js": [
            {
                "path": 'core_website_app/admin/js/user_requests.js',
                "is_raw": False
            },
        ],
    }

    modals = [
        'core_website_app/admin/account_requests/modals/deny_request.html',
    ]

    return render(request, 'core_website_app/admin/user_requests.html',
                  assets=assets, modals=modals,
                  context={'requests': requests})


@staff_member_required
def contact_messages(request):
    """ List messages from the contact page

        Args:
            request:

        Returns:
    """

    # Call the API
    messages_contact = contact_message_api.get_all()

    assets = {
        "js": [
            {
                "path": 'core_website_app/admin/js/messages.js',
                "is_raw": False
            },
        ],
    }

    modals = [
        'core_website_app/admin/contact_messages/modals/delete_message.html',
    ]

    return render(request, 'core_website_app/admin/contact_messages.html',
                  assets=assets, modals=modals,
                  context={'contacts': messages_contact})


class WebSiteInfoView(View):
    form_class = TextAreaForm
    api = None
    get_redirect = None
    post_redirect = None
    web_page_type = None

    def get(self, request, *args, **kwargs):
        """ GET request. Create/Show the form for the configuration.

        Args:
            request:
            *args:
            **kwargs:

        Returns:

        """
        website_object = self.api.get()
        content = website_object.content if website_object is not None else ''
        form = self.form_class({'content': content})

        return render(request, self.get_redirect, context={'form': form})

    def post(self, request, *args, **kwargs):
        """ POST request. Try to save the configuration.

        Args:
            request:
            *args:
            **kwargs:

        Returns:

        """
        form = self.form_class(request.POST)

        if form.is_valid():
            # Call the API
            content = request.POST['content']
            page = self.api.get()

            if page is None:
                page = WebPage(self.web_page_type, content)
            else:
                page.content = content

            self.api.upsert(page)
            messages.add_message(request, messages.INFO, 'Information saved with success.')

            return redirect(reverse(self.post_redirect))
