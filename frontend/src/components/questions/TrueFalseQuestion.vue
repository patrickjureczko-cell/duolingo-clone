<template>
  <div class="flex flex-col gap-3">
    <p class="text-xl font-bold text-duo-dark text-center mb-4">{{ question.text }}</p>
    <div class="flex gap-4">
      <button
        v-for="option in ['true', 'false']"
        :key="option"
        class="flex-1 py-5 rounded-2xl border-2 font-extrabold text-lg transition-all uppercase"
        :class="btnClass(option)"
        :disabled="!!selected"
        @click="select(option)"
      >
        {{ option === 'true' ? '✓ True' : '✗ False' }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import type { Question } from '../../api/types'

const props = defineProps<{ question: Question; correctAnswer?: string }>()
const emit = defineEmits<{ answer: [value: string] }>()

const selected = ref<string | null>(null)

function select(val: string) {
  if (selected.value) return
  selected.value = val
  emit('answer', val)
}

function btnClass(option: string) {
  if (!selected.value) {
    return option === 'true'
      ? 'border-duo-blue text-duo-blue hover:bg-blue-50'
      : 'border-duo-orange text-duo-orange hover:bg-orange-50'
  }
  if (option === props.correctAnswer) return 'border-duo-green bg-green-50 text-duo-green'
  if (option === selected.value) return 'border-duo-red bg-red-50 text-duo-red'
  return 'border-duo-light-gray text-duo-gray opacity-60'
}
</script>
