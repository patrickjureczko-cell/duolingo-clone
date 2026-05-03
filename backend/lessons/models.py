from django.db import models
import uuid


class LessonSession(models.Model):
    session_id = models.UUIDField()
    unit = models.ForeignKey('courses.Unit', on_delete=models.CASCADE, related_name='lesson_sessions')
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    xp_earned = models.PositiveIntegerField(default=0)
    hearts_lost = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'Session {self.session_id} – {self.unit}'


class Answer(models.Model):
    lesson = models.ForeignKey(LessonSession, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey('questions.Question', on_delete=models.CASCADE)
    given_answer = models.TextField()
    is_correct = models.BooleanField()
    answered_at = models.DateTimeField(auto_now_add=True)
