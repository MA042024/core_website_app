"""
    Admin views
"""
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from markdown import markdown
from core_main_app.utils.rendering import admin_render as render
from core_website_app.commons.constants import MARKDOWN_UNSAFE, MARKDOWN_GENERATION_FAILED, MARKDOWN_ERRORS, \
    UNKNOWN_ERROR
from core_website_app.templatetags.stripjs import stripjs
from core_website_app.views.admin.forms import TextAreaForm
from core_website_app.components.web_page.models import WebPage
import core_website_app.components.account_request.api as account_request_api
import core_website_app.components.contact_message.api as contact_message_api
from django.views.generic import View
from xml_utils.commons.exceptions import HTMLError
from xml_utils.html_tree.parser import parse_html


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

    @method_decorator(staff_member_required)
    def get(self, request, **kwargs):
        """ GET request. Create/Show the form for the configuration.

        Args:
            request:
            **kwargs:

        Returns:

        """
        if "current_content" in kwargs:
            content = kwargs["current_content"]
        else:
            website_object = self.api.get()
            content = website_object.content if website_object is not None else ''

        context = {
            "form": self.form_class({'content': content})
        }

        if "error_id" in kwargs:
            if kwargs["error_id"] < len(MARKDOWN_ERRORS):
                context["error_msg"] = MARKDOWN_ERRORS[kwargs["error_id"]]
            else:
                context["error_msg"] = UNKNOWN_ERROR

        assets = {
            "css": [
                "core_website_app/admin/css/style.css"
            ]
        }

        return render(request, self.get_redirect, context=context, assets=assets)

    @method_decorator(staff_member_required)
    def post(self, request):
        """ POST request. Try to save the configuration.

        Args:
            request:

        Returns:

        """
        form = self.form_class(request.POST)

        if form.is_valid():
            # Call the API
            content = request.POST['content']
            page = self.api.get()

            markdown_content = markdown(content)
            if markdown_content != stripjs(markdown_content):
                return self.get(request, current_content=content, error_id=MARKDOWN_UNSAFE)

            try:
                parse_html(markdown_content, 'div')
            except HTMLError:
                return self.get(request, current_content=content, error_id=MARKDOWN_GENERATION_FAILED)

            if page is None:
                page = WebPage(self.web_page_type, content)
            else:
                page.content = content

            self.api.upsert(page)
            messages.add_message(request, messages.INFO, 'Information saved with success.')

            return redirect(reverse(self.post_redirect))
