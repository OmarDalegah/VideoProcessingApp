from rest_framework import serializers
from operations.models import VideoRequest


class VideoRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoRequest
        fields = '__all__'
