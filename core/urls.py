from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/clearcache/", include("clearcache.urls")),
    path("admin/", admin.site.urls),
    path(r"^admin_tools/", include("admin_tools.urls")),
    path("ckeditor/", include("ckeditor_uploader.urls")),
    path("", include("blog.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
