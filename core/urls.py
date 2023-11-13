""" core URL Configuration """

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('chat/', include('chat.urls')),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('', RedirectView.as_view(url='/chat/')),

]


# Development
if bool(settings.DEBUG):
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)