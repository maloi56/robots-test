from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated

from robots.serializers import RobotsSerializer


class RobotModalViewSet(CreateModelMixin, GenericViewSet):
    """
            Предоставляет функциональность для приема новых роботов.

            Пример входных данных:

                {"serial":2, "model":"R2","version":"D2"}
            Или

                [{"serial":3, "model":"R3","version":"D3"}, {"serial: 2", "model":"R2","version":"D2"}]

            Доступен только авторизованным пользователям
        """

    serializer_class = RobotsSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs['data'], list):
            return super().get_serializer(many=True, *args, **kwargs)
        return super().get_serializer(*args, **kwargs)