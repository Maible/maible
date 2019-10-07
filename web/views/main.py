from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import FormView

from web.forms import LoginForm

__all__ = ["index_view", "LoginView", "logout_view"]


def index_view(request):
    return render(request, "index.html")


class LoginView(FormView):
    template_name = "login.html"
    form_class = LoginForm

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse("index"))
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("index")


@login_required()
def logout_view(request):
    logout(request)
    return redirect(reverse("index"))
