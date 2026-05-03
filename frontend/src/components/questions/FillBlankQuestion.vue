<template>
  <div class="flex flex-col gap-5">
    <p class="text-xl font-extrabold text-duo-dark text-center leading-relaxed">
      {{ beforeBlank }}
      <span class="inline-block border-b-4 min-w-[120px] mx-1 pb-0.5 align-bottom text-center"
        :class="result ? (result.is_correct ? 'border-duo-green text-duo-green' : 'border-duo-red text-duo-red') : 'border-duo-dark'">
        {{ answer || '      ' }}
      </span>
      {{ afterBlank }}
    </p>

    <input v-if="!result" v-model="answer" type="text" placeholder="Antwort eingeben…"
      class="w-full border-2 border-duo-light-gray rounded-2xl px-5 py-4 text-center font-bold text-lg focus:outline-none focus:border-duo-blue"
      @keydown.enter="submit"
    />

    <div v-if="result && !result.is_correct" class="text-center text-sm font-bold text-duo-gray">
      Correct answer: <span class="text-duo-green">{{ question.correct_answer }}</span>
    </div>

    <button v-if="!result" class="btn-primary w-full" :disabled="!answer.trim()" @click="submit">
      Antwort prüfen
    </button>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import type { Question, AnswerResult } from '../../api/types'

const props = defineProps<{ question: Question; result?: AnswerResult }>()
const emit = defineEmits<{ answer: [value: string] }>()

const answer = ref('')
const parts = computed(() => props.question.text.split('___'))
const beforeBlank = computed(() => parts.value[0] ?? '')
const afterBlank = computed(() => parts.value[1] ?? '')

function submit() {
  if (!answer.value.trim() || props.result) return
  emit('answer', answer.value.trim())
}
</script>
