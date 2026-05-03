<template>
  <div class="flex flex-col gap-4">
    <p class="text-xl font-extrabold text-duo-dark text-center leading-snug mb-2">{{ question.text }}</p>
    <button
      v-for="choice in question.choices"
      :key="choice"
      class="w-full text-left px-5 py-4 rounded-2xl border-2 font-bold transition-all text-base"
      :class="choiceClass(choice)"
      :disabled="!!result"
      @click="emit('answer', choice)"
    >
      {{ choice }}
    </button>
  </div>
</template>

<script setup lang="ts">
import type { Question, AnswerResult } from '../../api/types'

const props = defineProps<{ question: Question; result?: AnswerResult }>()
const emit = defineEmits<{ answer: [value: string] }>()

function choiceClass(choice: string) {
  if (!props.result) return 'border-duo-light-gray text-duo-dark hover:border-duo-blue hover:bg-blue-50 cursor-pointer'
  if (choice === props.result.correct_answer) return 'border-duo-green bg-green-50 text-duo-green'
  return 'border-duo-light-gray text-duo-gray opacity-50'
}
</script>
