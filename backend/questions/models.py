from django.db import models


class QuestionType(models.TextChoices):
    MCQ = 'MCQ', 'Multiple Choice'
    FILL_BLANK = 'FILL_BLANK', 'Fill in the Blank'
    TRUE_FALSE = 'TRUE_FALSE', 'True or False'
    FLASHCARD = 'FLASHCARD', 'Flashcard'


class Question(models.Model):
    unit = models.ForeignKey('courses.Unit', on_delete=models.CASCADE, related_name='questions')
    type = models.CharField(max_length=20, choices=QuestionType.choices)
    text = models.TextField()
    choices = models.JSONField(null=True, blank=True)  # list of strings, MCQ only
    correct_answer = models.TextField()
    explanation = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'[{self.type}] {self.text[:60]}'
