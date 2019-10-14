from django import forms
from django.contrib.auth import authenticate
from django.utils.translation import ugettext as _
from django.contrib.auth import get_user_model

__all__ = ["LoginForm", "MailboxAddForm", "RegistrationForm"]


class LoginForm(forms.Form):
    username = forms.CharField(label=_("Username"), required=True, max_length=150)
    password = forms.CharField(label=_("Password"), required=True, max_length=128, widget=forms.PasswordInput())

    def clean(self):
        super().clean()
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError(_("Incorrect Credentials!"))
        if not user.is_active:
            raise forms.ValidationError(_("User is disabled!"))


class RegistrationForm(forms.Form):
    first_name = forms.CharField(label=_("First name"), required=False, max_length=30)
    last_name = forms.CharField(label=_("Last name"), required=False, max_length=150)
    username = forms.CharField(label=_("Username"), required=True, max_length=150)
    password = forms.CharField(label=_("Password"), required=True, max_length=128, widget=forms.PasswordInput())

    def clean_username(self):
        username = self.cleaned_data["username"]
        username = username.lower().strip()
        if get_user_model().objects.filter(username=username).exists():
            raise forms.ValidationError(_("A user with this username already exists!"), code="invalid")
        return username


class MailboxAddForm(forms.Form):
    PROTOCOL_CHOICES = (
        ("pop3", "POP3"),
        ("pop3+ssl", "POP3 with SSL"),
        ("imap", "IMAP"),
        ("imap+ssl", "IMAP with SSL"),
        ("imap+tls", "IMAP with TLS (STARTTLS)"),
    )
    name = forms.CharField(
        label=_("Name"),
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={"class": "form", "placeholder": "Name of the mailbox"}),
    )
    protocol = forms.ChoiceField(
        label=_("Protocol"),
        required=True,
        choices=PROTOCOL_CHOICES,
        initial="imap",
        widget=forms.Select(attrs={"class": "form"}),
    )
    username = forms.CharField(
        label=_("Username"),
        required=True,
        max_length=50,
        widget=forms.TextInput(attrs={"class": "form", "placeholder": "Username"}),
    )
    password = forms.CharField(
        label=_("Password"),
        required=True,
        max_length=100,
        widget=forms.PasswordInput(attrs={"class": "form", "placeholder": "Password"}),
    )
    domain = forms.CharField(
        label=_("Domain (Server)"),
        required=True,
        max_length=90,
        widget=forms.TextInput(attrs={"class": "form", "placeholder": "example: imap.itu.edu.tr:993"}),
    )
    from_email = forms.EmailField(
        label=_("Sender email"),
        required=True,
        max_length=255,
        widget=forms.EmailInput(attrs={"class": "form", "placeholder": "Sender email address"}),
    )
