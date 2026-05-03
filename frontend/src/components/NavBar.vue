<template>
  <nav class="bg-white border-b-2 border-duo-light-gray sticky top-0 z-10">
    <div class="max-w-2xl mx-auto px-4 h-14 flex items-center justify-between">
      <RouterLink to="/" class="text-duo-green font-extrabold text-2xl tracking-tight">
        LearnFlow
      </RouterLink>
      <div class="flex items-center gap-4">
        <span class="flex items-center gap-1 font-bold text-duo-orange">
          🔥 {{ topStreak }}
        </span>
        <span class="flex items-center gap-1 font-bold text-yellow-500">
          ⭐ {{ totalXp }}
        </span>
        <RouterLink to="/upload" class="text-sm font-bold text-duo-blue hover:underline">
          + Upload
        </RouterLink>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useProgressStore } from '../stores/progressStore'

const progress = useProgressStore()

onMounted(() => progress.fetchAll())

const totalXp = computed(() => progress.allProgress.reduce((sum, p) => sum + p.xp, 0))
const topStreak = computed(() => Math.max(0, ...progress.allProgress.map((p) => p.streak_days)))
</script>
