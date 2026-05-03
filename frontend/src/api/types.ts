export interface Topic {
  id: number
  name: string
  icon: string
  description: string
  color: string
  course_count: number
}

export interface Unit {
  id: number
  title: string
  order: number
  question_count: number
}

export interface Course {
  id: number
  topic: number
  title: string
  description: string
  order: number
  units: Unit[]
}

export type QuestionType = 'MCQ' | 'FILL_BLANK' | 'TRUE_FALSE' | 'FLASHCARD'

export interface Question {
  id: number
  type: QuestionType
  text: string
  choices: string[] | null
  correct_answer: string
  explanation: string
  order: number
}

export interface LessonStart {
  lesson_id: number
  unit: string
  questions: Question[]
}

export interface AnswerResult {
  is_correct: boolean
  correct_answer: string
  explanation: string
  hearts_remaining: number
}

export interface LessonComplete {
  xp_earned: number
  total_xp: number
  streak_days: number
  hearts_remaining: number
  correct_count: number
  total_questions: number
}

export interface UserProgress {
  id: number
  topic: number
  topic_name: string
  topic_icon: string
  xp: number
  streak_days: number
  last_active: string | null
  hearts: number
  completed_unit_ids: number[]
}

export type UploadStatus = 'pending' | 'processing' | 'done' | 'failed'

export interface Upload {
  id: number
  original_filename: string
  topic: number
  course_title: string
  status: UploadStatus
  course: number | null
  questions_created: number
  error_message: string
  created_at: string
  completed_at: string | null
}
