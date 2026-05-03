from rest_framework import serializers
from .models import Topic


class TopicSerializer(serializers.ModelSerializer):
    course_count = serializers.SerializerMethodField()

    class Meta:
        model = Topic
        fields = ['id', 'name', 'icon', 'description', 'color', 'course_count']

    def get_course_count(self, obj):
        return obj.courses.count()
