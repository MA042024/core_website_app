"""
"""
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from .forms import HelpForm, PrivacyPolicyForm, TermsOfUseForm
from core_website_app.components.account_request.api import request_list
from core_website_app.components.contact_message.api import message_list
from core_website_app.components.privacy_policy.api import privacy_policy_get, privacy_policy_post
from core_website_app.components.terms_of_use.api import terms_of_use_get, terms_of_use_post
from core_website_app.components.help.api import help_get, help_post


@staff_member_required
def user_requests(request):
    """ Page that allows to accept or deny user requests

    :param request:
    :return:
    """

    # Call the API
    requests = request_list()

    return render(request, 'core_website_app/admin/user_requests.html', {'requests': requests})


@staff_member_required
def contact_messages(request):
    """ List messages from the contact page
    
    :param request:
    :return:
    """

    # Call the API
    messages_contact = message_list()

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
            help_post(request.POST['content'])
            messages.add_message(request, messages.INFO, 'Help saved with success.')
            return redirect('/admin/website')
    else:
        help = help_get()
        content = help.content if help is not None else ''
        form = HelpForm({'content': content})

    return render(request, 'core_website_app/admin/help.html', {'form': form})


@staff_member_required
def privacy_policy_admin(request):
    """
    Page that allows to edit Privacy Policy
    :param request:
    :return:
    """

    if request.method == 'POST':
        form = PrivacyPolicyForm(request.POST)
        if form.is_valid():
            # Call the API
            privacy_policy_post(request.POST['content'])
            messages.add_message(request, messages.INFO, 'Privacy Policy saved with success.')
            return redirect('/admin/website')
    else:
        policy = privacy_policy_get()
        content = policy.content if policy is not None else ''
        form = PrivacyPolicyForm({'content': content})

    return render(request, 'core_website_app/admin/privacy_policy.html', {'form': form})


@staff_member_required
def terms_of_use_admin(request):
    """
    Page that allows to edit Terms of Use
    :param request:
    :return:
    """

    if request.method == 'POST':
        form = TermsOfUseForm(request.POST)
        if form.is_valid():
            # Call the API
            terms_of_use_post(request.POST['content'])
            messages.add_message(request, messages.INFO, 'Terms of Use saved with success.')
            return redirect('/admin/website')
    else:
        terms = terms_of_use_get()
        content = terms.content if terms is not None else ''
        form = TermsOfUseForm({'content': content})

    return render(request, 'core_website_app/admin/terms_of_use.html', {'form': form})


@staff_member_required
def website(request):
    """
    Page that allows to edit website pages
    :param request:
    :return:
    """

    return render(request, 'core_website_app/admin/website.html', {})
