from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from core.views import test_session

urlpatterns = [
    path("", include("shops.urls")),
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
    path("accounts/", include("accounts.urls")),
    path("test-session/", test_session, name="test_session"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
