import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import client from '../api/client'
import { sessionId } from '../api/client'
import type { Question, AnswerResult, LessonComplete } from '../api/types'

export const useLessonStore = defineStore('lesson', () => {
  const lessonId = ref<number | null>(null)
  const unitTitle = ref('')
  const questions = ref<Question[]>([])
  const currentIndex = ref(0)
  const hearts = ref(5)
  const answers = ref<{ questionId: number; correct: boolean }[]>([])
  const lastResult = ref<AnswerResult | null>(null)
  const complete = ref<LessonComplete | null>(null)
  const loading = ref(false)

  const currentQuestion = computed(() => questions.value[currentIndex.value] ?? null)
  const isFinished = computed(() => currentIndex.value >= questions.value.length)
  const progressPct = computed(() =>
    questions.value.length ? (currentIndex.value / questions.value.length) * 100 : 0,
  )

  async function startLesson(unitId: number) {
    loading.value = true
    const { data } = await client.post('/lessons/start/', { unit_id: unitId, session_id: sessionId })
    lessonId.value = data.lesson_id
    unitTitle.value = data.unit
    questions.value = data.questions
    currentIndex.value = 0
    hearts.value = 5
    answers.value = []
    lastResult.value = null
    complete.value = null
    loading.value = false
  }

  async function submitAnswer(answer: string): Promise<AnswerResult> {
    const q = currentQuestion.value!
    const { data } = await client.post<AnswerResult>(`/lessons/${lessonId.value}/answer/`, {
      question_id: q.id,
      answer,
    })
    lastResult.value = data
    hearts.value = data.hearts_remaining
    answers.value.push({ questionId: q.id, correct: data.is_correct })
    return data
  }

  function advance() {
    lastResult.value = null
    currentIndex.value++
  }

  async function finishLesson(): Promise<LessonComplete> {
    const { data } = await client.post<LessonComplete>(`/lessons/${lessonId.value}/complete/`)
    complete.value = data
    return data
  }

  return {
    lessonId, unitTitle, questions, currentIndex, hearts, answers,
    lastResult, complete, loading,
    currentQuestion, isFinished, progressPct,
    startLesson, submitAnswer, advance, finishLesson,
  }
})
