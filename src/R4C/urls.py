from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from robots.urls import router
from users.views import IndexView
from .yasg import urlpatterns as doc_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('users/', include('users.urls', namespace='users')),
    path('store/', include('store.urls', namespace='store')),
]

urlpatterns += router.urls
urlpatterns += doc_urls

if settings.DEBUG:
    import mimetypes
    mimetypes.add_type("application/javascript", ".js", True)
    urlpatterns.append(path('__debug__/', include('debug_toolbar.urls')))
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
