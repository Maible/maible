from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext as _
from django_mailbox.models import Mailbox


__all__ = ["UserMailbox"]


class UserMailbox(models.Model):
    mailbox = models.OneToOneField(
        Mailbox, on_delete=models.CASCADE, related_name="user", primary_key=True
    )
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="mailboxes"
    )

    created_on = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        verbose_name = _("User Mailbox")
        verbose_name_plural = _("User Mailboxes")
        ordering = ("user",)

    def __str__(self):
        return self.user.__str__()
