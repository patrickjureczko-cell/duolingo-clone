from rest_framework import viewsets
from .models import Question
from .serializers import QuestionSerializer


class QuestionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = QuestionSerializer

    def get_queryset(self):
        qs = Question.objects.all()
        unit_id = self.request.query_params.get('unit')
        if unit_id:
            qs = qs.filter(unit_id=unit_id)
        return qs
