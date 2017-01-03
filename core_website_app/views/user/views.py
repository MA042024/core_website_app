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
from core_website_app.components.contact_message.models import ContactMessage
from core_website_app.views.user.forms import LoginForm
from .forms import RequestAccountForm, ContactForm
from core_website_app.components.account_request.models import AccountRequest
import core_website_app.components.account_request.api as account_request_api
import core_website_app.components.contact_message.api as contact_message_api
import core_website_app.components.help.api as help_api
import core_website_app.components.privacy_policy.api as privacy_policy_api
import core_website_app.components.terms_of_use.api as terms_of_use_api
import core_website_app.common.exceptions as exceptions


def homepage(request):
    """ Homepage for the website

        Parameters:
            request:

        Returns:
    """
    assets = {
        "js": []
    }

    if finders.find("core_website_app/css/homepage.css") is not None:
        assets["css"] = ["core_website_app/css/homepage.css"]

    if finders.find("core_website_app/js/homepage.js") is not None:
        assets["js"].append(
            {
                "path": "core_website_app/js/homepage.js",
                "is_raw": False
            }
        )

    if finders.find("core_website_app/js/homepage.raw.js") is not None:
        assets["js"].append(
            {
                "path": "core_website_app/js/homepage.raw.js",
                "is_raw": True
            }
        )

    return render(request, "core_website_app/user/homepage.html", assets=assets)


def request_new_account(request):
    """Page that allows to request a user account

        Parameters:
            request:

        Returns: Http response
    """

    if request.method == 'POST':
        request_form = RequestAccountForm(request.POST)
        if request_form.is_valid():
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
            except exceptions.WebsiteViewsError, e:
                message = e.message
                return render(request, 'request_new_account.html',
                              context={'request_form': request_form, 'action_result': message})
    else:
        request_form = RequestAccountForm()

    context = {
        "request_form": request_form
    }

    assets = {
        "js": [
            {
                "path": "core_website_app/user/js/user_account_req.js",
                "is_raw": False
            }
        ],
    }

    return render(request, 'core_website_app/user/request_new_account.html', assets=assets, context=context)


def contact(request):
    """Contact form

        Parameters:
            request:

        Returns: Http response
    """

    if request.method == 'POST':
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            # Call the API
            contact_message = ContactMessage(
                name=request.POST["name"],
                email=request.POST["email"],
                content=request.POST["message"],
            )

            contact_message_api.upsert(contact_message)
            messages.add_message(request, messages.INFO, 'Your message has been sent to the administrator.')
            return redirect('/')
    else:
        contact_form = ContactForm()

    return render(request, 'core_website_app/user/contact.html', context={'contact_form': contact_form})


def help_page(request):
    """Page that provides FAQ

        Parameters:
            request: Http response

        Returns:
    """
    # Call the API
    help_content = help_api.get()

    return render(request, 'core_website_app/user/help.html', context={'help': help_content})


def privacy_policy(request):
    """Page that provides privacy policy

        Parameters:
            request:

        Returns: Http response
    """

    # Call the API
    policy = privacy_policy_api.get()

    return render(request, 'core_website_app/user/privacy-policy.html', context={'policy': policy})


def terms_of_use(request):
    """Page that provides terms of use

        Parameters:
            request:

        Returns: Http Response
    """
    # Call the API
    terms = terms_of_use_api.get()

    return render(request, 'core_website_app/user/terms-of-use.html', context={'terms': terms})


def custom_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        try:
            user = authenticate(username=username, password=password)
            login(request, user)

            return redirect(reverse("core_website_homepage"))
        except Exception as e:
            return render(request, "core_website_app/user/login.html",
                          context={'login_form': LoginForm(), 'login_error': True})
    elif request.method == "GET":
        if request.user.is_authenticated():
            return redirect(reverse("core_website_homepage"))

        return render(request, "core_website_app/user/login.html", context={'login_form': LoginForm()})
    else:
        return HttpResponse(status=HTTP_405_METHOD_NOT_ALLOWED)


def custom_logout(request):
    logout(request)
    return redirect(reverse("core_website_login"))
