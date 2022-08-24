""" Form needed for the user part of everything
"""
from captcha.fields import CaptchaField
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RequestAccountForm(UserCreationForm):
    """
    Form to request an account
    """

    username = forms.CharField(label="Username", max_length=100, required=True)
    firstname = forms.CharField(label="First Name", max_length=100, required=True)
    lastname = forms.CharField(label="Last Name", max_length=100, required=True)
    email = forms.EmailField(label="Email Address", max_length=100, required=True)
    captcha = CaptchaField()

    class Meta:
        """Meta"""

        model = User
        fields = (
            "username",
            "firstname",
            "lastname",
            "email",
            "password1",
            "password2",
        )


class ContactForm(forms.Form):
    """
    Form to contact the administrator
    """

    name = forms.CharField(label="Name", max_length=100, required=True)
    email = forms.EmailField(label="Email Address", max_length=100, required=True)
    message = forms.CharField(
        label="Message",
        widget=forms.Textarea(attrs={"class": "textarea_lock_h"}),
        required=True,
    )
    captcha = CaptchaField()
