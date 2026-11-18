"""
URL configuration for ShareFood project.
"""
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # Endpoint used by the language switcher form
    path("i18n/", include("django.conf.urls.i18n")),
]

# All site pages get a language prefix: /en/..., /ru/..., /ro/...
urlpatterns += i18n_patterns(
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path("listings/", include("listings.urls", namespace='listings')),
    path("accounts/", include("accounts.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
)

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
