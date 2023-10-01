from rest_framework import serializers

from robots.models import Robot


class RobotsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Robot
        exclude = ('id', 'created',)
