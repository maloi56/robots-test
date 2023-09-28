from django.contrib import admin
from django.urls import include, path

from users.views import IndexView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('users/', include('users.urls', namespace='users')),
]
