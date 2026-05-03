from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import UserProgress
from .serializers import UserProgressSerializer


@api_view(['GET'])
def session_progress(request, session_id):
    progress = UserProgress.objects.filter(session_id=session_id).select_related('topic')
    return Response(UserProgressSerializer(progress, many=True).data)


@api_view(['GET'])
def topic_progress(request, session_id, topic_id):
    try:
        progress = UserProgress.objects.get(session_id=session_id, topic_id=topic_id)
        return Response(UserProgressSerializer(progress).data)
    except UserProgress.DoesNotExist:
        return Response({'xp': 0, 'streak_days': 0, 'hearts': 5, 'completed_unit_ids': []})
