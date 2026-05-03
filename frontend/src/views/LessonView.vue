<template>
  <div v-if="lesson.loading" class="min-h-screen flex items-center justify-center bg-white">
    <div class="flex flex-col items-center gap-4">
      <div class="w-12 h-12 border-4 border-duo-green border-t-transparent rounded-full animate-spin" />
      <div class="font-bold text-duo-gray">Lektion wird geladen…</div>
    </div>
  </div>

  <div v-else-if="lesson.complete" class="min-h-screen flex flex-col items-center justify-center bg-white px-6 text-center">
    <div class="text-7xl mb-4 animate-bounce">🎉</div>
    <h1 class="text-3xl font-extrabold text-duo-dark mb-1">Lektion abgeschlossen!</h1>
    <p class="text-duo-gray font-semibold mb-8">{{ lesson.unitTitle }}</p>

    <div class="grid grid-cols-3 gap-4 w-full max-w-xs mb-10">
      <div class="card p-4 text-center">
        <div class="text-2xl font-extrabold text-yellow-500">+{{ lesson.complete.xp_earned }}</div>
        <div class="text-xs font-bold text-duo-gray uppercase mt-1">XP</div>
      </div>
      <div class="card p-4 text-center">
        <div class="text-2xl font-extrabold text-duo-green">
          {{ lesson.complete.correct_count }}/{{ lesson.complete.total_questions }}
        </div>
        <div class="text-xs font-bold text-duo-gray uppercase mt-1">Richtig</div>
      </div>
      <div class="card p-4 text-center">
        <div class="text-2xl font-extrabold text-duo-orange">{{ lesson.complete.streak_days }}</div>
        <div class="text-xs font-bold text-duo-gray uppercase mt-1">🔥 Serie</div>
      </div>
    </div>

    <div class="w-full max-w-xs mb-8">
      <div class="flex justify-between text-xs font-bold text-duo-gray mb-1">
        <span>Genauigkeit</span>
        <span>{{ Math.round((lesson.complete.correct_count / lesson.complete.total_questions) * 100) }}%</span>
      </div>
      <div class="h-3 bg-duo-light-gray rounded-full overflow-hidden">
        <div class="h-full bg-duo-green rounded-full transition-all duration-1000"
          :style="{ width: (lesson.complete.correct_count / lesson.complete.total_questions * 100) + '%' }" />
      </div>
    </div>

    <div class="flex gap-3 w-full max-w-xs">
      <RouterLink to="/" class="btn-secondary flex-1 text-center">Startseite</RouterLink>
      <button class="btn-primary flex-1" @click="restart">Nochmal</button>
    </div>
  </div>

  <div v-else class="min-h-screen flex flex-col bg-white">
    <div class="px-4 pt-5 pb-3 flex items-center gap-3 border-b border-duo-light-gray">
      <button class="text-duo-gray hover:text-duo-red transition-colors p-1 rounded-full" @click="router.back()">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M6 18L18 6M6 6l12 12"/>
        </svg>
      </button>
      <div class="flex-1 bg-duo-light-gray rounded-full h-4 overflow-hidden">
        <div class="h-full bg-duo-green rounded-full transition-all duration-700 ease-out"
          :style="{ width: lesson.progressPct + '%' }" />
      </div>
      <div class="flex items-center gap-0.5">
        <span v-for="i in 5" :key="i" class="text-base leading-none transition-all"
          :class="i <= lesson.hearts ? 'grayscale-0' : 'grayscale opacity-30'">❤️</span>
      </div>
    </div>

    <div class="flex-1 flex flex-col max-w-lg mx-auto w-full px-5 pt-6 pb-4">
      <div class="text-xs font-extrabold uppercase text-duo-gray tracking-widest mb-5 text-center">
        Frage {{ lesson.currentIndex + 1 }} von {{ lesson.questions.length }}
      </div>
      <Transition name="slide" mode="out-in">
        <div :key="lesson.currentQuestion?.id" class="flex-1">
          <MCQQuestion v-if="lesson.currentQuestion?.type === 'MCQ'"
            :question="lesson.currentQuestion" :result="lesson.lastResult ?? undefined" @answer="onAnswer" />
          <TrueFalseQuestion v-else-if="lesson.currentQuestion?.type === 'TRUE_FALSE'"
            :question="lesson.currentQuestion" :result="lesson.lastResult ?? undefined" @answer="onAnswer" />
          <FillBlankQuestion v-else-if="lesson.currentQuestion?.type === 'FILL_BLANK'"
            :question="lesson.currentQuestion" :result="lesson.lastResult ?? undefined" @answer="onAnswer" />
          <FlashCard v-else-if="lesson.currentQuestion?.type === 'FLASHCARD'"
            :question="lesson.currentQuestion" @answer="onAnswer" />
        </div>
      </Transition>
    </div>

    <Transition name="slide-up">
      <div v-if="lesson.lastResult" class="px-5 py-5 border-t-2"
        :class="lesson.lastResult.is_correct ? 'bg-green-50 border-duo-green' : 'bg-red-50 border-duo-red'">
        <div class="max-w-lg mx-auto">
          <div class="flex items-start gap-3 mb-3">
            <div class="text-2xl">{{ lesson.lastResult.is_correct ? '✅' : '❌' }}</div>
            <div>
              <div class="font-extrabold text-lg"
                :class="lesson.lastResult.is_correct ? 'text-duo-green' : 'text-duo-red'">
                {{ lesson.lastResult.is_correct ? 'Richtig!' : 'Falsch' }}
              </div>
              <div v-if="!lesson.lastResult.is_correct" class="text-sm font-semibold text-duo-dark mt-0.5">
                Richtige Antwort: <strong>{{ lesson.lastResult.correct_answer }}</strong>
              </div>
              <div v-if="lesson.lastResult.explanation" class="text-sm text-duo-gray mt-1">
                {{ lesson.lastResult.explanation }}
              </div>
            </div>
          </div>
          <button class="btn-primary w-full" @click="advance">Weiter</button>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useLessonStore } from '../stores/lessonStore'
import MCQQuestion from '../components/questions/MCQQuestion.vue'
import TrueFalseQuestion from '../components/questions/TrueFalseQuestion.vue'
import FillBlankQuestion from '../components/questions/FillBlankQuestion.vue'
import FlashCard from '../components/questions/FlashCard.vue'

const route = useRoute()
const router = useRouter()
const lesson = useLessonStore()

onMounted(() => lesson.startLesson(Number(route.params.unitId)))

async function onAnswer(value: string) {
  await lesson.submitAnswer(value)
  if (lesson.hearts <= 0) await lesson.finishLesson()
}
async function advance() {
  lesson.advance()
  if (lesson.isFinished) await lesson.finishLesson()
}
function restart() {
  lesson.startLesson(Number(route.params.unitId))
}
</script>

<style scoped>
.slide-enter-active, .slide-leave-active { transition: all 0.2s ease; }
.slide-enter-from { opacity: 0; transform: translateX(24px); }
.slide-leave-to   { opacity: 0; transform: translateX(-24px); }
.slide-up-enter-active, .slide-up-leave-active { transition: all 0.25s ease; }
.slide-up-enter-from { opacity: 0; transform: translateY(16px); }
.slide-up-leave-to   { opacity: 0; }
</style>
