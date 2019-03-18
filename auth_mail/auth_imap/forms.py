# Global imports:
from django import forms
from django.utils.translation import gettext_lazy as _

# Local Imports:
from utils.config import server_list


class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        imap_server_list = [(s['label'], s['name'])
                            for s in server_list()]

        self.fields['host'].choices = imap_server_list

    host = forms.ChoiceField(
        label=_('Imap Server'),
        required=False,)
    username = forms.CharField(
        label=_('Username'),
        required=False,
        max_length=30,)
    password = forms.CharField(
        label=_('Password'),
        required=False,
        widget=forms.PasswordInput,
        max_length=40)
    next = forms.CharField(
        required=False,
        widget=forms.HiddenInput,
        max_length=256)