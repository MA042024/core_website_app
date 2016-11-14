"""
    Views available for the user
"""
from core_main_app.utils.rendering import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.staticfiles import finders
from django.core.urlresolvers import reverse
from django.http.response import HttpResponse
from django.shortcuts import redirect
from django.contrib import messages
from rest_framework.status import HTTP_405_METHOD_NOT_ALLOWED

from core_website_app.views.user.forms import LoginForm
from .forms import RequestAccountForm, ContactForm

from core_website_app.common.exceptions import ViewsWebsiteError
from core_website_app.components.account_request.models import AccountRequest
import core_website_app.components.account_request.api as account_request_api
import core_website_app.components.contact_message.api as contact_message_api
import core_website_app.components.help.api as help_api
import core_website_app.components.privacy_policy.api as privacy_policy_api
import core_website_app.components.terms_of_use.api as terms_of_use_api


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
                account_request = AccountRequest(request.POST['username'],
                                                 request.POST['firstname'],
                                                 request.POST['lastname'],
                                                 request.POST['password'],
                                                 request.POST['email'])

                account_request_api.insert(account_request)

                messages.add_message(request, messages.INFO, 'User Account Request sent to the administrator.')
                return redirect('/')
            except ViewsWebsiteError, e:
                message = e.message
                return render(request, 'request_new_account.html', {'form': form, 'action_result': message})
    else:
        form = RequestAccountForm()

    context = {
        "js": [
            "core_website_app/user/js/user_account_req.js"
        ],
        "form": form
    }

    return render(request, 'core_website_app/user/request_new_account.html', context)


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
            contact_message_api.save(request.POST['name'], request.POST['email'], request.POST['message'])
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
    help_content = help_api.get()

    return render(request, 'core_website_app/user/help.html', {'help': help_content})


def privacy_policy(request):
    """
    Page that provides privacy policy
    :param request:
    :return:
    """

    # Call the API
    policy = privacy_policy_api.get()

    return render(request, 'core_website_app/user/privacy-policy.html', {'policy': policy})


def terms_of_use(request):
    """
    Page that provides terms of use
    :param request:
    :return:
    """

    # Call the API
    terms = terms_of_use_api.get()

    return render(request, 'core_website_app/user/terms-of-use.html', {'terms': terms})


def custom_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        try:
            user = authenticate(username=username, password=password)
            login(request, user)

            return redirect(reverse("core_website_homepage"))
        except Exception as e:
            return render(request, "core_website_app/user/login.html", {'form': LoginForm(), 'login_error': True})
    elif request.method == "GET":
        if request.user.is_authenticated():
            return redirect(reverse("core_website_homepage"))

        return render(request, "core_website_app/user/login.html", {'form': LoginForm()})
    else:
        return HttpResponse(status=HTTP_405_METHOD_NOT_ALLOWED)


def custom_logout(request):
    logout(request)
    return redirect(reverse("core_website_login"))
