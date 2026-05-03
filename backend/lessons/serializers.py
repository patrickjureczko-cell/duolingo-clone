from rest_framework import serializers
from .models import LessonSession, Answer


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'question', 'given_answer', 'is_correct', 'answered_at']


class LessonSessionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = LessonSession
        fields = ['id', 'session_id', 'unit', 'started_at', 'completed_at', 'xp_earned', 'hearts_lost', 'answers']
