from django.contrib import admin
from web.models import UserMailbox


@admin.register(UserMailbox)
class UserMailboxAdmin(admin.ModelAdmin):
    list_display = ("mailbox", "user", "created_on")
    list_filter = ("created_on",)
    search_fields = ("user__email", "user__username")
