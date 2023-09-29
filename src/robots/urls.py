from django.urls import path, include

from rest_framework import routers
from robots.views import RobotModalViewSet

app_name = 'robots'

router = routers.DefaultRouter()
router.register(r'api/robots', RobotModalViewSet, basename='robots')

urlpatterns = [
    path('', include(router.urls)),
]