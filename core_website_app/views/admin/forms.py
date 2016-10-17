"""
"""
from django import forms


class PrivacyPolicyForm(forms.Form):
    """ Form to update the privacy policy
    """
    content = forms.CharField(label="Privacy Policy", widget=forms.Textarea, required=False)


class TermsOfUseForm(forms.Form):
    """ Form to update the terms of use
    """
    content = forms.CharField(label="Terms of Use", widget=forms.Textarea, required=False)


class HelpForm(forms.Form):
    """ Form to update the help
    """
    content = forms.CharField(label="Help", widget=forms.Textarea, required=False)
