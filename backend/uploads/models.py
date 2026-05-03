from django.db import models


class UploadStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    PROCESSING = 'processing', 'Processing'
    DONE = 'done', 'Done'
    FAILED = 'failed', 'Failed'


class Upload(models.Model):
    session_id = models.UUIDField()
    file = models.FileField(upload_to='uploads/')
    original_filename = models.CharField(max_length=255)
    topic = models.ForeignKey('topics.Topic', on_delete=models.SET_NULL, null=True, related_name='uploads')
    course_title = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=UploadStatus.choices, default=UploadStatus.PENDING)
    course = models.ForeignKey('courses.Course', on_delete=models.SET_NULL, null=True, blank=True, related_name='source_uploads')
    questions_created = models.PositiveIntegerField(default=0)
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.original_filename} ({self.status})'
