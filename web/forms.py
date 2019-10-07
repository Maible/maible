from django import forms
from django.contrib.auth import authenticate
from django.utils.translation import ugettext as _

__all__ = ["LoginForm", "MailboxAddForm"]


class LoginForm(forms.Form):
    username = forms.CharField(label=_("Username"), required=True, max_length=150)
    password = forms.CharField(
        label=_("Password"), required=True, max_length=128, widget=forms.PasswordInput()
    )

    def clean(self):
        super().clean()
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError(_("Incorrect Credentials!"))
        if not user.is_active:
            raise forms.ValidationError(_("User is disabled!"))


class MailboxAddForm(forms.Form):
    PROTOCOL_CHOICES = (
        ("pop3", "POP3"),
        ("pop3+ssl", "POP3 with SSL"),
        ("imap", "IMAP"),
        ("imap+ssl", "IMAP with SSL"),
        ("imap+tls", "IMAP with TLS (STARTTLS)"),
    )
    name = forms.CharField(label=_("Name"), max_length=255, required=True)
    protocol = forms.ChoiceField(
        label=_("Protocol"), required=True, choices=PROTOCOL_CHOICES, initial="imap"
    )
    username = forms.CharField(label=_("Username"), required=True, max_length=50)
    password = forms.CharField(
        label=_("Password"), required=True, max_length=100, widget=forms.PasswordInput()
    )
    domain = forms.CharField(label=_("Domain (Server)"), required=True, max_length=90)
    from_email = forms.EmailField(
        label=_("Sender email"), required=True, max_length=255
    )
