from django.db import models


class Topic(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=10)  # emoji
    description = models.TextField()
    color = models.CharField(max_length=7, default='#58CC02')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
