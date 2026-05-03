from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import LessonSession, Answer
from .serializers import LessonSessionSerializer
from courses.models import Unit
from questions.models import Question
from questions.serializers import QuestionSerializer
from progress.models import UserProgress


HEARTS_START = 5
XP_PER_CORRECT = 10
XP_LESSON_BONUS = 20


@api_view(['POST'])
def start_lesson(request):
    unit_id = request.data.get('unit_id')
    session_id = request.data.get('session_id')
    if not unit_id or not session_id:
        return Response({'error': 'unit_id and session_id are required'}, status=400)

    unit = Unit.objects.get(pk=unit_id)
    lesson = LessonSession.objects.create(session_id=session_id, unit=unit)
    questions = unit.questions.all()
    return Response({
        'lesson_id': lesson.id,
        'unit': unit.title,
        'questions': QuestionSerializer(questions, many=True).data,
    })


@api_view(['POST'])
def submit_answer(request, lesson_id):
    lesson = LessonSession.objects.get(pk=lesson_id)
    question_id = request.data.get('question_id')
    given_answer = request.data.get('answer', '').strip()

    question = Question.objects.get(pk=question_id)
    is_correct = given_answer.lower() == question.correct_answer.lower()

    Answer.objects.create(lesson=lesson, question=question, given_answer=given_answer, is_correct=is_correct)

    if not is_correct:
        lesson.hearts_lost = min(lesson.hearts_lost + 1, HEARTS_START)
        lesson.save(update_fields=['hearts_lost'])

    return Response({
        'is_correct': is_correct,
        'correct_answer': question.correct_answer,
        'explanation': question.explanation,
        'hearts_remaining': HEARTS_START - lesson.hearts_lost,
    })


@api_view(['POST'])
def complete_lesson(request, lesson_id):
    lesson = LessonSession.objects.get(pk=lesson_id)
    if lesson.completed_at:
        return Response(LessonSessionSerializer(lesson).data)

    correct_count = lesson.answers.filter(is_correct=True).count()
    xp = correct_count * XP_PER_CORRECT + XP_LESSON_BONUS
    lesson.xp_earned = xp
    lesson.completed_at = timezone.now()
    lesson.save(update_fields=['xp_earned', 'completed_at'])

    session_id = str(lesson.session_id)
    topic = lesson.unit.course.topic
    progress, _ = UserProgress.objects.get_or_create(session_id=lesson.session_id, topic=topic)

    today = timezone.now().date()
    if progress.last_active == today:
        pass
    elif progress.last_active and (today - progress.last_active).days == 1:
        progress.streak_days += 1
    else:
        progress.streak_days = 1

    progress.xp += xp
    progress.last_active = today
    progress.hearts = max(0, HEARTS_START - lesson.hearts_lost)
    progress.completed_units.add(lesson.unit)
    progress.save()

    return Response({
        'xp_earned': xp,
        'total_xp': progress.xp,
        'streak_days': progress.streak_days,
        'hearts_remaining': progress.hearts,
        'correct_count': correct_count,
        'total_questions': lesson.answers.count(),
    })
