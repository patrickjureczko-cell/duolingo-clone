from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Course, Unit
from .serializers import CourseSerializer, UnitDetailSerializer
from topics.models import Topic


class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CourseSerializer

    def get_queryset(self):
        qs = Course.objects.prefetch_related('units')
        topic_id = self.request.query_params.get('topic')
        if topic_id:
            qs = qs.filter(topic_id=topic_id)
        return qs

    @action(detail=False, url_path='unit/(?P<unit_id>[^/.]+)')
    def unit_detail(self, request, unit_id=None):
        unit = Unit.objects.prefetch_related('questions').get(pk=unit_id)
        return Response(UnitDetailSerializer(unit).data)
