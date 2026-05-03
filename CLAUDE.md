# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A Duolingo-style topic learning app where users select a domain (e.g. IT, Dentistry, Mechanics) and complete lessons generated from uploaded source material (PDFs, ebooks). Claude AI extracts questions from uploaded files. The stack is Vue 3 + TypeScript (frontend) and Django + PostgreSQL (backend), self-hosted.

## Repository Layout

```
duolingo-clone/
├── frontend/          # Vue 3 + TypeScript, built with Vite
└── backend/           # Django + Django REST Framework
```

## Frontend Commands

```bash
cd frontend
npm install
npm run dev          # dev server at http://localhost:5173
npm run build        # production build to dist/
npm run type-check   # tsc --noEmit
npm run lint         # eslint
npm run test         # vitest
npm run test -- --run src/path/to/file.spec.ts   # single test file
```

## Backend Commands

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env                # then fill in values

python manage.py migrate
python manage.py runserver          # API at http://localhost:8000

python manage.py test               # all tests
python manage.py test topics.tests  # single app
pytest -k test_name                 # single test (if pytest is configured)
```

## Environment Variables (backend `.env`)

```
DATABASE_URL=postgres://user:pass@localhost:5432/duolingo_clone
ANTHROPIC_API_KEY=sk-ant-...
MEDIA_ROOT=/path/to/media          # uploaded files land here
ALLOWED_HOSTS=localhost,127.0.0.1
DEBUG=True
```

## Architecture

### Backend Django Apps

| App | Responsibility |
|-----|----------------|
| `topics` | Topic catalogue (IT, Dentistry, etc.) and user topic enrollment |
| `courses` | Courses within a topic; ordered unit/lesson structure |
| `questions` | Question bank — MCQ, fill-in-blank, true/false, flashcard types |
| `lessons` | Lesson sessions: delivers questions, records answers |
| `progress` | XP, streaks, hearts/lives, per-user per-topic stats |
| `uploads` | File upload model + Celery task that calls Claude to extract questions |

### File Upload → Question Extraction Flow

1. User uploads a PDF/ebook via `POST /api/uploads/`.
2. Django saves the file to `MEDIA_ROOT` and creates an `Upload` record.
3. A Celery task calls the Anthropic API (Claude) with the extracted text, instructing it to return structured JSON: question text, type, choices, correct answer, and optional explanation.
4. The task creates `Question` objects from the JSON response and links them to the relevant `Course`.
5. Frontend polls `GET /api/uploads/{id}/status/` until `status == "done"`.

### Gamification Model (mirrors Duolingo)

- **XP**: awarded per correct answer and on lesson completion; stored on `UserProgress`.
- **Streaks**: daily login/lesson-completion check; `UserProgress.streak_days` incremented by a daily cron/Celery beat task.
- **Hearts**: users start with 5; each wrong answer costs 1; refill over time or via XP. Enforced in the lesson session logic, not the question model.
- **Lessons**: fixed number of questions per session; progress bar advances per answer; "lesson complete" screen on finish.

### Frontend State (Pinia stores)

| Store | Manages |
|-------|---------|
| `topicStore` | Available topics, enrolled topics |
| `lessonStore` | Active lesson session state — current question, answer history, hearts remaining |
| `progressStore` | XP total, streak, hearts — synced from backend on app load |
| `uploadStore` | Upload status polling |

### API Conventions

- All endpoints under `/api/`.
- DRF serializers live beside their model in `<app>/serializers.py`.
- Use DRF `ViewSet`s registered with a `DefaultRouter`.
- Dates/times in ISO 8601 UTC. Scores and XP as integers.

### Frontend → Backend Communication

- Axios instance in `frontend/src/api/client.ts` with `baseURL` pointing to the Django dev server; in production both are served from the same origin via nginx.
- No auth headers for now; session is anonymous, identified by a UUID stored in `localStorage` and sent as `X-Session-ID` header.

## Key Design Decisions

- **No auth**: user identity is a UUID session token for now; all progress is keyed to this UUID.
- **Claude for extraction**: the prompt should request structured JSON output (use Claude's tool-use / structured output feature) so parsing is reliable.
- **Local file storage**: `django.core.files.storage.FileSystemStorage` pointing at `MEDIA_ROOT`; no S3.
- **Celery + Redis** for async question extraction; Redis also serves as the Celery broker.
- **Question types**: `MCQ`, `FILL_BLANK`, `TRUE_FALSE`, `FLASHCARD` — stored as a `type` enum on the `Question` model; the frontend renders a different component per type.
