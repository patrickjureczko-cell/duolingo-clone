<template>
  <aside class="fixed left-0 top-0 h-full w-64 bg-white border-r-2 border-duo-light-gray flex flex-col py-6 px-4 z-20">
    <RouterLink to="/" class="flex items-center gap-2 mb-10 px-2">
      <span class="text-3xl">🎓</span>
      <span class="text-duo-green font-extrabold text-2xl tracking-tight">LearnFlow</span>
    </RouterLink>

    <nav class="flex flex-col gap-1 flex-1">
      <RouterLink v-for="item in navItems" :key="item.to" :to="item.to"
        class="flex items-center gap-3 px-4 py-3 rounded-2xl font-bold text-duo-gray hover:bg-gray-50 transition-colors"
        active-class="bg-duo-green/10 !text-duo-green"
      >
        <span class="text-2xl">{{ item.icon }}</span>
        <span>{{ item.label }}</span>
      </RouterLink>
    </nav>

    <!-- Stats -->
    <div class="border-t-2 border-duo-light-gray pt-4 mt-4 flex flex-col gap-3">
      <div class="flex items-center gap-3 px-4">
        <span class="text-2xl">🔥</span>
        <div>
          <div class="font-extrabold text-duo-dark">{{ topStreak }} day streak</div>
          <div class="text-xs text-duo-gray font-semibold">Keep it up!</div>
        </div>
      </div>
      <div class="flex items-center gap-3 px-4">
        <span class="text-2xl">⭐</span>
        <div>
          <div class="font-extrabold text-duo-dark">{{ totalXp }} XP</div>
          <div class="text-xs text-duo-gray font-semibold">Total earned</div>
        </div>
      </div>
    </div>
  </aside>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useProgressStore } from '../stores/progressStore'

const progress = useProgressStore()
onMounted(() => progress.fetchAll())

const totalXp = computed(() => progress.allProgress.reduce((s, p) => s + p.xp, 0))
const topStreak = computed(() => Math.max(0, ...progress.allProgress.map((p) => p.streak_days)))

const navItems = [
  { to: '/', icon: '🏠', label: 'Learn' },
  { to: '/upload', icon: '📄', label: 'Upload Material' },
]
</script>
