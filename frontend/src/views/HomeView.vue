<template>
  <div class="max-w-2xl mx-auto px-4 py-8 pb-24 lg:pb-8">
    <div class="mb-8">
      <h1 class="text-3xl font-extrabold text-duo-dark">Was möchtest du lernen?</h1>
      <p class="text-duo-gray font-semibold mt-1">Wähle ein Thema und starte deine Lernreise</p>
    </div>

    <div v-if="store.loading" class="grid grid-cols-1 sm:grid-cols-2 gap-4">
      <div v-for="i in 6" :key="i" class="card p-5 h-28 animate-pulse bg-gray-100" />
    </div>

    <div v-else class="grid grid-cols-1 sm:grid-cols-2 gap-4">
      <RouterLink
        v-for="topic in store.topics"
        :key="topic.id"
        :to="`/topic/${topic.id}`"
        class="card p-5 flex items-center gap-4 hover:shadow-md transition-all hover:-translate-y-0.5 active:translate-y-0"
      >
        <div class="w-14 h-14 rounded-2xl flex items-center justify-center text-3xl flex-shrink-0"
          :style="{ background: topic.color + '22' }">{{ topic.icon }}</div>
        <div class="flex-1 min-w-0">
          <div class="font-extrabold text-duo-dark text-base leading-tight">{{ topic.name }}</div>
          <div class="text-xs text-duo-gray mt-0.5 line-clamp-1">{{ topic.description }}</div>
          <div class="mt-2 flex items-center gap-2">
            <div class="flex-1 h-2 bg-duo-light-gray rounded-full overflow-hidden">
              <div class="h-full rounded-full transition-all duration-500"
                :style="{ width: xpBarWidth(topic.id), background: topic.color }" />
            </div>
            <span class="text-xs font-bold" :style="{ color: topic.color }">
              {{ progressStore.getForTopic(topic.id)?.xp ?? 0 }} XP
            </span>
          </div>
        </div>
        <div class="text-duo-light-gray text-xl font-bold flex-shrink-0">›</div>
      </RouterLink>
    </div>

    <div class="mt-8 card p-6 flex items-center gap-4 bg-gradient-to-r from-duo-blue/10 to-purple-100 border-duo-blue/30">
      <div class="w-14 h-14 rounded-2xl bg-duo-blue/20 flex items-center justify-center text-3xl flex-shrink-0">📄</div>
      <div class="flex-1">
        <div class="font-extrabold text-duo-dark">Eigenes Material hochladen</div>
        <div class="text-sm text-duo-gray">PDF oder Textdatei → KI erstellt eine komplette Lektion</div>
      </div>
      <RouterLink to="/upload" class="btn-primary !py-2 !px-4 !text-xs whitespace-nowrap">Starten</RouterLink>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useTopicStore } from '../stores/topicStore'
import { useProgressStore } from '../stores/progressStore'

const store = useTopicStore()
const progressStore = useProgressStore()

onMounted(() => Promise.all([store.fetchTopics(), progressStore.fetchAll()]))

function xpBarWidth(topicId: number) {
  const xp = progressStore.getForTopic(topicId)?.xp ?? 0
  return Math.min(100, (xp / 500) * 100) + '%'
}
</script>
