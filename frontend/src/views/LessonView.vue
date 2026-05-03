<template>
  <!-- Loading -->
  <div v-if="lesson.loading" class="min-h-screen flex items-center justify-center">
    <div class="w-12 h-12 border-4 border-duo-green border-t-transparent rounded-full animate-spin" />
  </div>

  <!-- Lesson complete screen -->
  <div v-else-if="lesson.complete" class="min-h-screen flex flex-col items-center justify-center px-6 text-center">
    <div class="text-7xl mb-4">🎉</div>
    <h1 class="text-3xl font-extrabold text-duo-dark mb-1">Lesson Complete!</h1>
    <p class="text-duo-gray font-semibold mb-8">{{ lesson.unitTitle }}</p>

    <div class="flex gap-6 mb-10">
      <div class="text-center">
        <div class="text-3xl font-extrabold text-yellow-500">⭐ {{ lesson.complete.xp_earned }}</div>
        <div class="text-xs font-bold uppercase text-duo-gray">XP Earned</div>
      </div>
      <div class="text-center">
        <div class="text-3xl font-extrabold text-duo-green">
          {{ lesson.complete.correct_count }}/{{ lesson.complete.total_questions }}
        </div>
        <div class="text-xs font-bold uppercase text-duo-gray">Correct</div>
      </div>
      <div class="text-center">
        <div class="text-3xl font-extrabold text-duo-orange">🔥 {{ lesson.complete.streak_days }}</div>
        <div class="text-xs font-bold uppercase text-duo-gray">Streak</div>
      </div>
    </div>

    <div class="flex gap-3">
      <RouterLink to="/" class="btn-secondary">Home</RouterLink>
      <button class="btn-primary" @click="restart">Practice Again</button>
    </div>
  </div>

  <!-- Active lesson -->
  <div v-else class="min-h-screen flex flex-col">
    <!-- Top bar -->
    <div class="px-4 pt-4 pb-2 flex items-center gap-3">
      <button class="text-duo-gray hover:text-duo-red font-bold text-xl p-1" @click="router.back()">✕</button>
      <div class="flex-1 bg-duo-light-gray rounded-full h-4 overflow-hidden">
        <div
          class="h-full bg-duo-green rounded-full transition-all duration-500"
          :style="{ width: lesson.progressPct + '%' }"
        />
      </div>
      <div class="flex items-center gap-0.5 text-sm font-bold">
        <span v-for="i in 5" :key="i" class="text-lg">
          {{ i <= lesson.hearts ? '❤️' : '🖤' }}
        </span>
      </div>
    </div>

    <!-- Question area -->
    <div class="flex-1 flex flex-col justify-between max-w-lg mx-auto w-full px-4 py-6">
      <div>
        <div class="text-xs font-bold uppercase text-duo-gray mb-6 text-center">
          Question {{ lesson.currentIndex + 1 }} of {{ lesson.questions.length }}
        </div>

        <Transition name="slide" mode="out-in">
          <div :key="lesson.currentQuestion?.id">
            <MCQQuestion
              v-if="lesson.currentQuestion?.type === 'MCQ'"
              :question="lesson.currentQuestion"
              :correct-answer="lesson.lastResult?.correct_answer"
              @answer="onAnswer"
            />
            <TrueFalseQuestion
              v-else-if="lesson.currentQuestion?.type === 'TRUE_FALSE'"
              :question="lesson.currentQuestion"
              :correct-answer="lesson.lastResult?.correct_answer"
              @answer="onAnswer"
            />
            <FillBlankQuestion
              v-else-if="lesson.currentQuestion?.type === 'FILL_BLANK'"
              :question="lesson.currentQuestion"
              :correct-answer="lesson.lastResult?.correct_answer"
              @answer="onAnswer"
            />
            <FlashCard
              v-else-if="lesson.currentQuestion?.type === 'FLASHCARD'"
              :question="lesson.currentQuestion"
              @answer="onAnswer"
            />
          </div>
        </Transition>
      </div>

      <!-- Feedback banner -->
      <Transition name="slide-up">
        <div
          v-if="lesson.lastResult"
          class="mt-6 rounded-2xl p-4"
          :class="lesson.lastResult.is_correct ? 'bg-green-50 border-2 border-duo-green' : 'bg-red-50 border-2 border-duo-red'"
        >
          <div class="font-extrabold text-lg mb-1" :class="lesson.lastResult.is_correct ? 'text-duo-green' : 'text-duo-red'">
            {{ lesson.lastResult.is_correct ? '✓ Correct!' : '✗ Incorrect' }}
          </div>
          <div v-if="!lesson.lastResult.is_correct" class="text-sm font-semibold text-duo-dark mb-1">
            Answer: <strong>{{ lesson.lastResult.correct_answer }}</strong>
          </div>
          <div v-if="lesson.lastResult.explanation" class="text-sm text-duo-gray">
            {{ lesson.lastResult.explanation }}
          </div>
          <button class="btn-primary mt-3 w-full" @click="advance">Continue</button>
        </div>
      </Transition>
    </div>
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
  if (lesson.hearts <= 0) {
    await lesson.finishLesson()
  }
}

async function advance() {
  lesson.advance()
  if (lesson.isFinished) {
    await lesson.finishLesson()
  }
}

function restart() {
  lesson.startLesson(Number(route.params.unitId))
}
</script>

<style scoped>
.slide-enter-active, .slide-leave-active { transition: all 0.2s ease; }
.slide-enter-from { opacity: 0; transform: translateX(30px); }
.slide-leave-to { opacity: 0; transform: translateX(-30px); }
.slide-up-enter-active, .slide-up-leave-active { transition: all 0.25s ease; }
.slide-up-enter-from { opacity: 0; transform: translateY(20px); }
.slide-up-leave-to { opacity: 0; transform: translateY(20px); }
</style>
