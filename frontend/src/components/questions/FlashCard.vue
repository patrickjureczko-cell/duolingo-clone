<template>
  <div class="flex flex-col gap-4">
    <!-- Card flip -->
    <div class="relative h-48 cursor-pointer" style="perspective: 1000px" @click="flipped = !flipped">
      <div
        class="absolute inset-0 rounded-2xl border-2 border-duo-light-gray flex items-center justify-center p-6 text-center transition-all duration-500"
        style="backface-visibility: hidden; transform-style: preserve-3d"
        :style="{ transform: flipped ? 'rotateY(180deg)' : 'rotateY(0deg)' }"
      >
        <div>
          <div class="text-xs font-bold uppercase text-duo-gray mb-2">Frage</div>
          <div class="text-lg font-bold text-duo-dark">{{ question.text }}</div>
          <div class="mt-4 text-xs text-duo-gray">Tippen zum Aufdecken</div>
        </div>
      </div>
      <div
        class="absolute inset-0 rounded-2xl border-2 border-duo-green bg-green-50 flex items-center justify-center p-6 text-center transition-all duration-500"
        style="backface-visibility: hidden; transform-style: preserve-3d; transform: rotateY(180deg)"
        :style="{ transform: flipped ? 'rotateY(0deg)' : 'rotateY(-180deg)' }"
      >
        <div>
          <div class="text-xs font-bold uppercase text-duo-green mb-2">Antwort</div>
          <div class="text-lg font-bold text-duo-dark">{{ question.correct_answer }}</div>
        </div>
      </div>
    </div>

    <div v-if="flipped && !answered" class="flex gap-3">
      <button class="flex-1 btn-danger" @click="respond(false)">✗ Wusste ich nicht</button>
      <button class="flex-1 btn-primary" @click="respond(true)">✓ Gewusst</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import type { Question } from '../../api/types'

const props = defineProps<{ question: Question }>()
const emit = defineEmits<{ answer: [value: string] }>()

const flipped = ref(false)
const answered = ref(false)

function respond(knew: boolean) {
  answered.value = true
  emit('answer', knew ? props.question.correct_answer : '')
}
</script>
