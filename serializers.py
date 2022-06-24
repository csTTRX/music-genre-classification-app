from rest_framework import serializers

class UploadSerializer(serializers.Serializer):
    file_name = serializers.FileField()