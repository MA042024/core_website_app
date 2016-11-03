""" Views available for the user
"""
from core_main_app.utils.rendering import render
from django.contrib.staticfiles import finders
from django.shortcuts import redirect
from django.contrib import messages
from core_main_app.commons.exceptions import MDCSError

from .forms import RequestAccountForm, ContactForm
from core_website_app.components.account_request.api import request_post
from core_website_app.components.contact_message.api import message_post
from core_website_app.components.help.api import help_get
from core_website_app.components.privacy_policy.api import privacy_policy_get
from core_website_app.components.terms_of_use.api import terms_of_use_get


def homepage(request):
    """ Homepage for the website

    :param request:
    :return:
    """
    context = {}

    if finders.find("core_website_app/css/homepage.css") is not None:
        context["css"] = ["core_website_app/css/homepage.css"]

    if finders.find("core_website_app/js/homepage.js") is not None:
        context["js"] = ["core_website_app/js/homepage.js"]

    return render(request, "core_website_app/user/homepage.html", context)


def request_new_account(request):
    """
    Page that allows to request a user account
    :param request:
    :return:
    """

    if request.method == 'POST':
        form = RequestAccountForm(request.POST)
        if form.is_valid():
            # call the API
            try:
                request_post(request.POST['username'],
                             request.POST['firstname'],
                             request.POST['lastname'],
                             request.POST['password'],
                             request.POST['email'])
                messages.add_message(request, messages.INFO, 'User Account Request sent to the administrator.')
                return redirect('/')
            except MDCSError, e:
                message = e.message
                return render(request, 'request_new_account.html', {'form': form, 'action_result': message})
    else:
        form = RequestAccountForm()

    return render(request, 'core_website_app/user/request_new_account.html', {'form': form})


def contact(request):
    """
    Contact form
    :param request:
    :return:
    """

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Call the API
            message_post(request.POST['name'], request.POST['email'], request.POST['message'])
            messages.add_message(request, messages.INFO, 'Your message has been sent to the administrator.')
            return redirect('/')
    else:
        form = ContactForm()

    return render(request, 'core_website_app/user/contact.html', {'form': form})


def help(request):
    """
    Page that provides FAQ
    :param request:
    :return:
    """

    # Call the API
    help_content = help_get()

    return render(request, 'core_website_app/user/help.html', {'help': help_content})


def privacy_policy(request):
    """
    Page that provides privacy policy
    :param request:
    :return:
    """

    # Call the API
    policy = privacy_policy_get()

    return render(request, 'core_website_app/user/privacy-policy.html', {'policy': policy})


def terms_of_use(request):
    """
    Page that provides terms of use
    :param request:
    :return:
    """

    # Call the API
    terms = terms_of_use_get()

    return render(request, 'core_website_app/user/terms-of-use.html', {'terms': terms})
