from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.urls import include, re_path


urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^api-auth/', include('rest_framework.urls')),

    re_path(r'^api/v1/auth/', include('api.v1.authentication.urls', namespace="api_v1_authentication")),
    re_path(r'^api/v1/posts/', include('api.v1.posts.urls', namespace="api_v1_posts")),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
