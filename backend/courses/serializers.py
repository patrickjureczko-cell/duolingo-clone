from rest_framework import serializers
from .models import Course, Unit
from questions.serializers import QuestionSerializer


class UnitSerializer(serializers.ModelSerializer):
    question_count = serializers.SerializerMethodField()

    class Meta:
        model = Unit
        fields = ['id', 'title', 'order', 'question_count']

    def get_question_count(self, obj):
        return obj.questions.count()


class UnitDetailSerializer(UnitSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta(UnitSerializer.Meta):
        fields = UnitSerializer.Meta.fields + ['questions']


class CourseSerializer(serializers.ModelSerializer):
    units = UnitSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'topic', 'title', 'description', 'order', 'units']
