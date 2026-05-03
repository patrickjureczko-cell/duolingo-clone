from django.db import models


class UserProgress(models.Model):
    session_id = models.UUIDField()
    topic = models.ForeignKey('topics.Topic', on_delete=models.CASCADE, related_name='user_progress')
    xp = models.PositiveIntegerField(default=0)
    streak_days = models.PositiveIntegerField(default=0)
    last_active = models.DateField(null=True, blank=True)
    hearts = models.PositiveIntegerField(default=5)
    completed_units = models.ManyToManyField('courses.Unit', blank=True)

    class Meta:
        unique_together = ('session_id', 'topic')

    def __str__(self):
        return f'{self.session_id} / {self.topic.name}'
