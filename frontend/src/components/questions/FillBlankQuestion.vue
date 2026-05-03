<template>
  <div class="flex flex-col gap-4">
    <p class="text-xl font-bold text-duo-dark text-center leading-relaxed">
      {{ beforeBlank }}
      <span class="inline-block border-b-2 border-duo-dark min-w-[100px] mx-1 align-bottom">
        <span v-if="submitted" :class="isCorrect ? 'text-duo-green' : 'text-duo-red'">{{ answer }}</span>
        <span v-else class="invisible">placeholder</span>
      </span>
      {{ afterBlank }}
    </p>
    <input
      v-if="!submitted"
      v-model="answer"
      type="text"
      placeholder="Type your answer…"
      class="w-full border-2 border-duo-light-gray rounded-xl px-4 py-3 text-center font-bold text-lg focus:outline-none focus:border-duo-blue"
      @keydown.enter="submit"
    />
    <div v-if="submitted && !isCorrect" class="text-center text-sm font-bold text-duo-gray">
      Correct answer: <span class="text-duo-green">{{ question.correct_answer }}</span>
    </div>
    <button v-if="!submitted" class="btn-primary" :disabled="!answer.trim()" @click="submit">
      Check
    </button>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import type { Question } from '../../api/types'

const props = defineProps<{ question: Question; correctAnswer?: string }>()
const emit = defineEmits<{ answer: [value: string] }>()

const answer = ref('')
const submitted = ref(false)
const isCorrect = ref(false)

const parts = computed(() => props.question.text.split('___'))
const beforeBlank = computed(() => parts.value[0] ?? '')
const afterBlank = computed(() => parts.value[1] ?? '')

function submit() {
  if (!answer.value.trim() || submitted.value) return
  submitted.value = true
  isCorrect.value = answer.value.trim().toLowerCase() === (props.correctAnswer ?? '').toLowerCase()
  emit('answer', answer.value.trim())
}
</script>
