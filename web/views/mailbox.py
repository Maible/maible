from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import FormView
from django_mailbox.models import Mailbox

from web.forms import MailboxAddForm
from web.models import UserMailbox

__all__ = ["mailbox_index", "CreateMailboxView"]


@login_required()
def mailbox_index(request):
    mailbox = request.user.mailboxes.first()
    if not mailbox:
        return redirect(reverse("add_mailbox"))
    return render(request, "mailbox/index.html", {"mailbox": mailbox})


class CreateMailboxView(LoginRequiredMixin, FormView):
    template_name = "mailbox/add.html"
    form_class = MailboxAddForm

    def form_valid(self, form):
        name = form.cleaned_data.get("name")
        protocol = form.cleaned_data.get("protocol")
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        domain = form.cleaned_data.get("domain")
        from_email = form.cleaned_data.get("from_email")
        mail_uri = f"{protocol}://{username}:{password}@{domain}"
        mailbox = Mailbox.objects.create(
            name=name, uri=mail_uri, from_email=from_email, active=True
        )
        UserMailbox.objects.create(user=self.request.user, mailbox=mailbox)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("mailbox_index")
