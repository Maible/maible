from django.conf import settings as django_settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from web import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.index_view, name='index')
]

if django_settings.DEBUG:
    urlpatterns += static(django_settings.MEDIA_URL, document_root=django_settings.MEDIA_ROOT)
    urlpatterns += static(django_settings.STATIC_URL, document_root=django_settings.STATIC_ROOT)
