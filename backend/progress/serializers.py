from rest_framework import serializers
from .models import UserProgress


class UserProgressSerializer(serializers.ModelSerializer):
    topic_name = serializers.CharField(source='topic.name', read_only=True)
    topic_icon = serializers.CharField(source='topic.icon', read_only=True)
    completed_unit_ids = serializers.SerializerMethodField()

    class Meta:
        model = UserProgress
        fields = ['id', 'topic', 'topic_name', 'topic_icon', 'xp', 'streak_days', 'last_active', 'hearts', 'completed_unit_ids']

    def get_completed_unit_ids(self, obj):
        return list(obj.completed_units.values_list('id', flat=True))
