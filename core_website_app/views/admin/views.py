"""
    Admin views
"""
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
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

    :param request:
    :return:
    """

    # Call the API
    requests = account_request_api.get_all()

    return render(request, 'core_website_app/admin/user_requests.html', {'requests': requests})


@staff_member_required
def contact_messages(request):
    """ List messages from the contact page
    
    :param request:
    :return:
    """

    # Call the API
    messages_contact = contact_message_api.get_all()

    return render(request, 'core_website_app/admin/contact_messages.html', {'contacts': messages_contact})


@staff_member_required
def help_admin(request):
    """
    Page that allows to edit Help
    :param request:
    :return:
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
            return redirect('/admin/website')
    else:
        help = help_api.get()
        content = help.content if help is not None else ''
        form = HelpForm({'content': content})

    return render(request, 'core_website_app/admin/help.html', {'form': form})


@staff_member_required
def privacy_policy_admin(request):
    """Page that allows to edit Privacy Policy

        Parameters:
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
            return redirect('/admin/website')
    else:
        policy = privacy_policy_api.get()
        content = policy.content if policy is not None else ''
        form = PrivacyPolicyForm({'content': content})

    return render(request, 'core_website_app/admin/privacy_policy.html', {'form': form})


@staff_member_required
def terms_of_use_admin(request):
    """Page that allows to edit Terms of Use

        Parameters:
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
                terms_of_use_page = WebPage(WEB_PAGE_TYPES["privacy_policy"], terms_of_use_content)
            else:
                terms_of_use_page.content = terms_of_use_content
            terms_of_use_api.upsert(terms_of_use_page)
            messages.add_message(request, messages.INFO, 'Terms of Use saved with success.')
            return redirect('/admin/website')
    else:
        terms = terms_of_use_api.get()
        content = terms.content if terms is not None else ''
        form = TermsOfUseForm({'content': content})

    return render(request, 'core_website_app/admin/terms_of_use.html', {'form': form})


@staff_member_required
def website(request):
    """Page that allows to edit website pages

        Parameters:
            request:

        Returns: Http Response
    """

    return render(request, 'core_website_app/admin/website.html', {})
