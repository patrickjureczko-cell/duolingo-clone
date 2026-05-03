<template>
  <div class="flex flex-col gap-6">
    <p class="text-xl font-extrabold text-duo-dark text-center leading-snug px-2">{{ question.text }}</p>
    <div class="flex gap-4">
      <button v-for="option in ['true', 'false']" :key="option"
        class="flex-1 py-6 rounded-2xl border-2 font-extrabold text-lg transition-all uppercase tracking-wide"
        :class="btnClass(option)"
        :disabled="!!result"
        @click="emit('answer', option)"
      >
        {{ option === 'true' ? '✓ True' : '✗ False' }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Question, AnswerResult } from '../../api/types'

const props = defineProps<{ question: Question; result?: AnswerResult }>()
const emit = defineEmits<{ answer: [value: string] }>()

function btnClass(option: string) {
  if (!props.result)
    return option === 'true'
      ? 'border-duo-blue text-duo-blue hover:bg-blue-50 cursor-pointer'
      : 'border-duo-orange text-duo-orange hover:bg-orange-50 cursor-pointer'
  if (option === props.result.correct_answer) return 'border-duo-green bg-green-50 text-duo-green'
  return 'border-duo-light-gray text-duo-gray opacity-50'
}
</script>
