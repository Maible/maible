from maible.base import INSTALLED_APPS, MIDDLEWARE  # NOQA

SECRET_KEY = '...'
DEBUG = False
DEBUG_TOOLBAR = False

TIME_ZONE = 'Europe/Istanbul'

# Email Settings
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = ""
EMAIL_PORT = 465
EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = ""
EMAIL_USE_SSL = True
# EMAIL_USE_TLS = False
DEFAULT_FROM_EMAIL = ""
DEFAULT_CONTACT_EMAIL = DEFAULT_FROM_EMAIL

ALLOWED_HOSTS = ["*"]
