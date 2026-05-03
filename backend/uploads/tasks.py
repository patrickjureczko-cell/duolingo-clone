import json
import logging
from celery import shared_task
from django.utils import timezone
from django.conf import settings

logger = logging.getLogger(__name__)

EXTRACT_FUNCTION = {
    "name": "save_questions",
    "description": "Save extracted questions from the educational material.",
    "parameters": {
        "type": "object",
        "properties": {
            "questions": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "type": {"type": "string", "enum": ["MCQ", "FILL_BLANK", "TRUE_FALSE", "FLASHCARD"]},
                        "text": {"type": "string"},
                        "choices": {"type": "array", "items": {"type": "string"}},
                        "correct_answer": {"type": "string"},
                        "explanation": {"type": "string"},
                    },
                    "required": ["type", "text", "correct_answer"],
                },
                "minItems": 5,
                "maxItems": 40,
            }
        },
        "required": ["questions"],
    },
}

SYSTEM_PROMPT = """Du bist ein erfahrener Ersteller von Lernmaterialien. Extrahiere aus dem gegebenen Lehrtext
eine abwechslungsreiche Sammlung von Fragen zu den wichtigsten Konzepten.
Erstelle eine Mischung aus Fragetypen: MCQ (Multiple Choice mit 4 Optionen), FILL_BLANK (Satz mit einer Lücke),
TRUE_FALSE und FLASHCARD (Begriff → Definition).
Bei MCQ genau 4 Antwortmöglichkeiten angeben. Bei FILL_BLANK ___ als Platzhalter verwenden.
Alle Fragen und Antworten auf Deutsch verfassen."""

GENERATE_SYSTEM_PROMPT = """Du bist ein erfahrener Ersteller von Lernmaterialien. Erstelle eine umfassende Sammlung
von Lernfragen zum angegebenen Thema.
Erstelle eine abwechslungsreiche Mischung: MCQ (4 Antworten), FILL_BLANK (___ als Lücke), TRUE_FALSE und
FLASHCARD (Begriff → Definition).
Decke Grundlagen, Fachbegriffe, praktisches Wissen und häufige Missverständnisse ab.
Alle Fragen und Antworten auf Deutsch verfassen."""


def extract_text_from_file(file_path: str) -> str:
    if file_path.lower().endswith('.pdf'):
        import pdfplumber
        text_parts = []
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages[:30]:
                text = page.extract_text()
                if text:
                    text_parts.append(text)
        return '\n\n'.join(text_parts)
    else:
        with open(file_path, 'r', errors='ignore') as f:
            return f.read(50_000)


def _call_openai_for_questions(prompt: str, system: str) -> list:
    from openai import OpenAI
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    response = client.chat.completions.create(
        model='gpt-4o',
        messages=[
            {'role': 'system', 'content': system},
            {'role': 'user', 'content': prompt},
        ],
        tools=[{'type': 'function', 'function': EXTRACT_FUNCTION}],
        tool_choice={'type': 'function', 'function': {'name': 'save_questions'}},
    )
    tool_call = response.choices[0].message.tool_calls[0]
    return json.loads(tool_call.function.arguments)['questions']


def _save_questions_to_unit(unit, questions_data: list) -> int:
    from questions.models import Question
    objs = [
        Question(
            unit=unit,
            type=q['type'],
            text=q['text'],
            choices=q.get('choices'),
            correct_answer=q['correct_answer'],
            explanation=q.get('explanation', ''),
            order=i,
        )
        for i, q in enumerate(questions_data)
    ]
    Question.objects.bulk_create(objs)
    return len(objs)


@shared_task(bind=True, max_retries=2)
def process_upload(self, upload_id: int):
    from .models import Upload, UploadStatus
    from courses.models import Course, Unit

    upload = Upload.objects.select_related('topic').get(pk=upload_id)
    upload.status = UploadStatus.PROCESSING
    upload.save(update_fields=['status'])

    try:
        text = extract_text_from_file(upload.file.path)
        if not text.strip():
            raise ValueError('Could not extract text from the uploaded file.')

        questions_data = _call_openai_for_questions(
            f'Extract questions from the following educational text:\n\n{text[:15_000]}',
            SYSTEM_PROMPT,
        )

        course = Course.objects.create(
            topic=upload.topic,
            title=upload.course_title,
            description=f'Auto-generated from {upload.original_filename}',
        )
        unit = Unit.objects.create(course=course, title='Lesson 1', order=0)
        count = _save_questions_to_unit(unit, questions_data)

        upload.status = UploadStatus.DONE
        upload.course = course
        upload.questions_created = count
        upload.completed_at = timezone.now()
        upload.save(update_fields=['status', 'course', 'questions_created', 'completed_at'])

    except Exception as exc:
        logger.exception('Failed to process upload %s', upload_id)
        upload.status = UploadStatus.FAILED
        upload.error_message = str(exc)
        upload.save(update_fields=['status', 'error_message'])
        raise self.retry(exc=exc, countdown=10)


@shared_task(bind=True, max_retries=2)
def generate_topic_course(self, upload_id: int, topic_name: str, course_title: str):
    from .models import Upload, UploadStatus
    from courses.models import Course, Unit

    upload = Upload.objects.select_related('topic').get(pk=upload_id)
    upload.status = UploadStatus.PROCESSING
    upload.save(update_fields=['status'])

    try:
        questions_data = _call_openai_for_questions(
            f'Generate 20 educational questions about: {topic_name}. Course title: {course_title}',
            GENERATE_SYSTEM_PROMPT,
        )

        course = Course.objects.create(
            topic=upload.topic,
            title=course_title,
            description=f'AI-generated course on {topic_name}',
        )
        unit = Unit.objects.create(course=course, title='Lesson 1', order=0)
        count = _save_questions_to_unit(unit, questions_data)

        upload.status = UploadStatus.DONE
        upload.course = course
        upload.questions_created = count
        upload.completed_at = timezone.now()
        upload.save(update_fields=['status', 'course', 'questions_created', 'completed_at'])

    except Exception as exc:
        logger.exception('Failed to generate topic course for upload %s', upload_id)
        upload.status = UploadStatus.FAILED
        upload.error_message = str(exc)
        upload.save(update_fields=['status', 'error_message'])
        raise self.retry(exc=exc, countdown=10)
