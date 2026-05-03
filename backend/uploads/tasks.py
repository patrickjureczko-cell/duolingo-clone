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

SYSTEM_PROMPT = """You are an expert educational content creator. Given text from an educational document,
extract a varied set of questions covering the key concepts.
Create a mix of question types: MCQ (multiple choice with 4 options), FILL_BLANK (sentence with one blank),
TRUE_FALSE, and FLASHCARD (concept → definition).
For MCQ, include exactly 4 choices. For FILL_BLANK, use ___ as the blank placeholder.
Keep questions clear, educational, and focused on important concepts."""


def extract_text_from_file(file_path: str) -> str:
    if file_path.lower().endswith('.pdf'):
        import pdfplumber
        text_parts = []
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages[:30]:  # cap at 30 pages
                text = page.extract_text()
                if text:
                    text_parts.append(text)
        return '\n\n'.join(text_parts)
    else:
        with open(file_path, 'r', errors='ignore') as f:
            return f.read(50_000)  # cap at 50k chars


@shared_task(bind=True, max_retries=2)
def process_upload(self, upload_id: int):
    from .models import Upload, UploadStatus
    from courses.models import Course, Unit
    from questions.models import Question

    upload = Upload.objects.select_related('topic').get(pk=upload_id)
    upload.status = UploadStatus.PROCESSING
    upload.save(update_fields=['status'])

    try:
        from openai import OpenAI

        text = extract_text_from_file(upload.file.path)
        if not text.strip():
            raise ValueError('Could not extract text from the uploaded file.')

        truncated = text[:15_000]

        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        response = client.chat.completions.create(
            model='gpt-4o',
            messages=[
                {'role': 'system', 'content': SYSTEM_PROMPT},
                {'role': 'user', 'content': f'Extract questions from the following educational text:\n\n{truncated}'},
            ],
            tools=[{'type': 'function', 'function': EXTRACT_FUNCTION}],
            tool_choice={'type': 'function', 'function': {'name': 'save_questions'}},
        )

        tool_call = response.choices[0].message.tool_calls[0]
        questions_data = json.loads(tool_call.function.arguments)['questions']

        course = Course.objects.create(
            topic=upload.topic,
            title=upload.course_title,
            description=f'Auto-generated from {upload.original_filename}',
        )
        unit = Unit.objects.create(course=course, title='Lesson 1', order=0)

        question_objs = [
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
        Question.objects.bulk_create(question_objs)

        upload.status = UploadStatus.DONE
        upload.course = course
        upload.questions_created = len(question_objs)
        upload.completed_at = timezone.now()
        upload.save(update_fields=['status', 'course', 'questions_created', 'completed_at'])

    except Exception as exc:
        logger.exception('Failed to process upload %s', upload_id)
        upload.status = UploadStatus.FAILED
        upload.error_message = str(exc)
        upload.save(update_fields=['status', 'error_message'])
        raise self.retry(exc=exc, countdown=10)
