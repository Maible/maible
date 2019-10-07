from django import forms
from django.contrib.auth import authenticate
from django.utils.translation import ugettext as _

__all__ = ["LoginForm"]


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
