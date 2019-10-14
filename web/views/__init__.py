from web.views.main import index_view, LoginView, logout_view, RegistrationView
from web.views.mailbox import mailbox_index, CreateMailboxView, mail_details

__all__ = [
    "index_view", "LoginView", "logout_view", "RegistrationView", "mailbox_index", "CreateMailboxView",
    "mail_details"
]
