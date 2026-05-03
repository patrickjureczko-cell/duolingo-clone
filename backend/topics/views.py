from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Topic
from .serializers import TopicSerializer


class TopicViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer


@api_view(['POST'])
def generate_course(request, topic_id):
    from uploads.models import Upload
    from uploads.tasks import generate_topic_course

    topic = Topic.objects.get(pk=topic_id)
    session_id = request.data.get('session_id')
    if not session_id:
        return Response({'error': 'session_id is required'}, status=400)

    existing_count = topic.courses.count()
    course_title = f'{topic.name} — Part {existing_count + 1}'

    upload = Upload.objects.create(
        session_id=session_id,
        file='',
        original_filename='AI Generated',
        topic=topic,
        course_title=course_title,
    )
    generate_topic_course.delay(upload.id, topic.name, course_title)
    return Response({'upload_id': upload.id, 'course_title': course_title})
