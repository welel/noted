from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.views.i18n import JavaScriptCatalog
from django.urls import path, include


urlpatterns = i18n_patterns(
    path("admin/", admin.site.urls),
    path("users/", include(("users.urls", "users"), namespace="users")),
    path("jsi18n/", JavaScriptCatalog.as_view(), name="javascript-catalog"),
    path("", include(("content.urls", "content"), namespace="content")),
)

if "rosetta" in settings.INSTALLED_APPS:
    urlpatterns.insert(1, path("rosetta/", include("rosetta.urls")))

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
