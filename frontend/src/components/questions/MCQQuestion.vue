<template>
  <div class="flex flex-col gap-3">
    <p class="text-xl font-bold text-duo-dark text-center mb-2">{{ question.text }}</p>
    <button
      v-for="choice in question.choices"
      :key="choice"
      class="w-full text-left px-5 py-4 rounded-2xl border-2 font-bold transition-all"
      :class="choiceClass(choice)"
      :disabled="!!selected"
      @click="select(choice)"
    >
      {{ choice }}
    </button>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import type { Question } from '../../api/types'

const props = defineProps<{ question: Question; revealed?: boolean; correctAnswer?: string }>()
const emit = defineEmits<{ answer: [value: string] }>()

const selected = ref<string | null>(null)

function select(choice: string) {
  if (selected.value) return
  selected.value = choice
  emit('answer', choice)
}

function choiceClass(choice: string) {
  if (!selected.value) return 'border-duo-light-gray text-duo-dark hover:border-duo-blue hover:bg-blue-50'
  if (choice === props.correctAnswer) return 'border-duo-green bg-green-50 text-duo-green'
  if (choice === selected.value) return 'border-duo-red bg-red-50 text-duo-red'
  return 'border-duo-light-gray text-duo-gray opacity-60'
}
</script>
