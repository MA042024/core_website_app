"""
    Admin views
"""
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from core_main_app.utils.rendering import admin_render as render
from .forms import HelpForm, PrivacyPolicyForm, TermsOfUseForm
from core_website_app.components.web_page.models import WebPage, WEB_PAGE_TYPES
import core_website_app.components.account_request.api as account_request_api
import core_website_app.components.contact_message.api as contact_message_api
import core_website_app.components.help.api as help_api
import core_website_app.components.privacy_policy.api as privacy_policy_api
import core_website_app.components.terms_of_use.api as terms_of_use_api


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


@staff_member_required
def help_admin(request):
    """
    Page that allows to edit Help

        Args:
            request:

        Returns:
    """
    if request.method == 'POST':
        form = HelpForm(request.POST)
        if form.is_valid():
            # Call the API
            help_content = request.POST['content']
            help_page = help_api.get()
            if help_page is None:
                help_page = WebPage(WEB_PAGE_TYPES["help"], help_content)
            else:
                help_page.content = help_content
            help_api.upsert(help_page)
            messages.add_message(request, messages.INFO, 'Help saved with success.')
            return redirect(reverse("admin:core_website_app_help"))
    else:
        help_page = help_api.get()
        content = help_page.content if help_page is not None else ''
        form = HelpForm({'content': content})

    return render(request, 'core_website_app/admin/help.html', context={'form': form})


@staff_member_required
def privacy_policy_admin(request):
    """Page that allows to edit Privacy Policy

        Args:
            request:

        Returns: Http response
    """
    if request.method == 'POST':
        form = PrivacyPolicyForm(request.POST)

        if form.is_valid():
            # Call the API
            privacy_policy_content = request.POST['content']
            privacy_policy_page = privacy_policy_api.get()

            if privacy_policy_page is None:
                privacy_policy_page = WebPage(WEB_PAGE_TYPES["privacy_policy"], privacy_policy_content)
            else:
                privacy_policy_page.content = privacy_policy_content

            privacy_policy_api.upsert(privacy_policy_page)
            messages.add_message(request, messages.INFO, 'Privacy Policy saved with success.')
            return redirect(reverse("admin:core_website_app_privacy"))
    else:
        policy = privacy_policy_api.get()
        content = policy.content if policy is not None else ''
        form = PrivacyPolicyForm({'content': content})

    return render(request, 'core_website_app/admin/privacy_policy.html', context={'form': form})


@staff_member_required
def terms_of_use_admin(request):
    """Page that allows to edit Terms of Use

        Args:
            request:

        Returns: Http response
    """
    if request.method == 'POST':
        form = TermsOfUseForm(request.POST)

        if form.is_valid():
            # Call the API
            terms_of_use_content = request.POST['content']
            terms_of_use_page = terms_of_use_api.get()

            if terms_of_use_page is None:
                terms_of_use_page = WebPage(WEB_PAGE_TYPES["terms_of_use"], terms_of_use_content)
            else:
                terms_of_use_page.content = terms_of_use_content
            terms_of_use_api.upsert(terms_of_use_page)
            messages.add_message(request, messages.INFO, 'Terms of Use saved with success.')

            return redirect(reverse("admin:core_website_app_terms"))
    else:
        terms = terms_of_use_api.get()
        content = terms.content if terms is not None else ''
        form = TermsOfUseForm({'content': content})

    return render(request, 'core_website_app/admin/terms_of_use.html', context={'form': form})
