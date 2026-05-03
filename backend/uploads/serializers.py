from rest_framework import serializers
from .models import Upload


class UploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Upload
        fields = ['id', 'original_filename', 'topic', 'course_title', 'status', 'course', 'questions_created', 'error_message', 'created_at', 'completed_at']
        read_only_fields = ['status', 'course', 'questions_created', 'error_message', 'completed_at']


class UploadCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Upload
        fields = ['file', 'topic', 'course_title', 'session_id']
