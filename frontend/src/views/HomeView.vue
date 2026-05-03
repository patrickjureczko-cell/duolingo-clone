<template>
  <main class="max-w-2xl mx-auto px-4 py-8">
    <div class="text-center mb-8">
      <h1 class="text-4xl font-extrabold text-duo-dark mb-2">What do you want to learn?</h1>
      <p class="text-duo-gray font-semibold">Choose a topic or upload your own material</p>
    </div>

    <div v-if="store.loading" class="flex justify-center py-16">
      <div class="w-10 h-10 border-4 border-duo-green border-t-transparent rounded-full animate-spin" />
    </div>

    <div v-else class="flex flex-col gap-3">
      <TopicCard
        v-for="topic in store.topics"
        :key="topic.id"
        :topic="topic"
        :progress="progressStore.getForTopic(topic.id)"
      />
    </div>

    <div class="mt-8 text-center">
      <RouterLink to="/upload" class="btn-secondary inline-block">
        📄 Upload your own material
      </RouterLink>
    </div>
  </main>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useTopicStore } from '../stores/topicStore'
import { useProgressStore } from '../stores/progressStore'
import TopicCard from '../components/TopicCard.vue'

const store = useTopicStore()
const progressStore = useProgressStore()

onMounted(async () => {
  await Promise.all([store.fetchTopics(), progressStore.fetchAll()])
})
</script>
