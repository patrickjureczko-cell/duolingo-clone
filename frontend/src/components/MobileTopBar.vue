<template>
  <header class="bg-white border-b-2 border-duo-light-gray px-4 h-14 flex items-center justify-between sticky top-0 z-10">
    <RouterLink to="/" class="flex items-center gap-1.5">
      <span class="text-xl">🎓</span>
      <span class="text-duo-green font-extrabold text-lg">LearnFlow</span>
    </RouterLink>
    <div class="flex items-center gap-4">
      <span class="font-extrabold text-duo-orange flex items-center gap-1">🔥 {{ topStreak }}</span>
      <span class="font-extrabold text-yellow-500 flex items-center gap-1">⭐ {{ totalXp }}</span>
    </div>
  </header>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useProgressStore } from '../stores/progressStore'

const progress = useProgressStore()
const totalXp = computed(() => progress.allProgress.reduce((s, p) => s + p.xp, 0))
const topStreak = computed(() => Math.max(0, ...progress.allProgress.map((p) => p.streak_days)))
</script>
