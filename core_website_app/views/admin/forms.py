"""
"""
from django import forms


class TextAreaForm(forms.Form):
    """ TextArea Form
    """
    content = forms.CharField(label="", widget=forms.Textarea(attrs={'class': 'form-control'}),
                              required=False)
