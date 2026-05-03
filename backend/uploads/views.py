from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import status
from .models import Upload
from .serializers import UploadSerializer
from .tasks import process_upload


@api_view(['POST'])
@parser_classes([MultiPartParser])
def create_upload(request):
    file = request.FILES.get('file')
    topic_id = request.data.get('topic_id')
    course_title = request.data.get('course_title', file.name if file else 'Untitled')
    session_id = request.data.get('session_id')

    if not file or not topic_id or not session_id:
        return Response({'error': 'file, topic_id, and session_id are required'}, status=400)

    upload = Upload.objects.create(
        session_id=session_id,
        file=file,
        original_filename=file.name,
        topic_id=topic_id,
        course_title=course_title,
    )
    process_upload.delay(upload.id)
    return Response(UploadSerializer(upload).data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def upload_status(request, upload_id):
    try:
        upload = Upload.objects.get(pk=upload_id)
    except Upload.DoesNotExist:
        return Response({'error': 'Not found'}, status=404)
    return Response(UploadSerializer(upload).data)
