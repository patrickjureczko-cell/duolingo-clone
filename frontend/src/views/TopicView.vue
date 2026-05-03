<template>
  <main class="max-w-2xl mx-auto px-4 py-8">
    <div v-if="loading" class="flex justify-center py-16">
      <div class="w-10 h-10 border-4 border-duo-green border-t-transparent rounded-full animate-spin" />
    </div>

    <template v-else>
      <!-- Header -->
      <div class="flex items-center gap-4 mb-6">
        <div
          class="w-14 h-14 rounded-2xl flex items-center justify-center text-3xl"
          :style="{ backgroundColor: (topic?.color ?? '#58CC02') + '22' }"
        >{{ topic?.icon }}</div>
        <div>
          <h1 class="text-2xl font-extrabold text-duo-dark">{{ topic?.name }}</h1>
          <p class="text-duo-gray text-sm">{{ topic?.description }}</p>
        </div>
      </div>

      <!-- Stats bar -->
      <div v-if="progress" class="card flex justify-around mb-6 py-4">
        <div class="text-center">
          <div class="text-2xl font-extrabold text-duo-orange">🔥 {{ progress.streak_days }}</div>
          <div class="text-xs text-duo-gray font-bold uppercase">Streak</div>
        </div>
        <div class="text-center">
          <div class="text-2xl font-extrabold text-yellow-500">⭐ {{ progress.xp }}</div>
          <div class="text-xs text-duo-gray font-bold uppercase">Total XP</div>
        </div>
        <div class="text-center">
          <div class="text-2xl font-extrabold text-duo-red">
            {{ '❤️'.repeat(progress.hearts) }}{{ '🖤'.repeat(5 - progress.hearts) }}
          </div>
          <div class="text-xs text-duo-gray font-bold uppercase">Hearts</div>
        </div>
      </div>

      <!-- Empty state -->
      <div v-if="courses.length === 0" class="text-center py-12">
        <div class="text-5xl mb-4">📚</div>
        <p class="text-duo-gray font-semibold mb-4">No courses yet for this topic.</p>
        <RouterLink to="/upload" class="btn-primary inline-block">Upload material</RouterLink>
      </div>

      <!-- Course / unit map -->
      <div v-for="course in courses" :key="course.id" class="mb-8">
        <h2 class="font-extrabold text-lg text-duo-dark mb-3 flex items-center gap-2">
          <span>{{ course.title }}</span>
          <span class="text-xs bg-duo-light-gray text-duo-gray px-2 py-0.5 rounded-full font-bold">
            {{ course.units.length }} unit{{ course.units.length !== 1 ? 's' : '' }}
          </span>
        </h2>

        <div class="relative flex flex-col items-center gap-2">
          <!-- Connecting line -->
          <div class="absolute left-1/2 top-0 bottom-0 w-0.5 bg-duo-light-gray -translate-x-1/2 z-0" />

          <div
            v-for="(unit, idx) in course.units"
            :key="unit.id"
            class="relative z-10 flex flex-col items-center"
            :class="idx % 2 === 0 ? 'self-start ml-[30%]' : 'self-end mr-[30%]'"
          >
            <button
              class="w-16 h-16 rounded-full border-b-4 font-extrabold text-white text-sm flex items-center justify-center shadow transition-transform hover:scale-105 active:scale-95"
              :class="isCompleted(unit.id)
                ? 'bg-duo-green border-duo-green-dark'
                : unit.question_count > 0
                  ? 'bg-duo-blue border-blue-700'
                  : 'bg-duo-gray border-gray-500 cursor-not-allowed'"
              :disabled="unit.question_count === 0"
              @click="goToLesson(unit.id)"
            >
              {{ isCompleted(unit.id) ? '✓' : idx + 1 }}
            </button>
            <div class="text-xs font-bold text-duo-gray mt-1 text-center max-w-[80px]">{{ unit.title }}</div>
          </div>
        </div>
      </div>
    </template>
  </main>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useTopicStore } from '../stores/topicStore'
import { useProgressStore } from '../stores/progressStore'
import type { Topic, Course, UserProgress } from '../api/types'

const route = useRoute()
const router = useRouter()
const topicStore = useTopicStore()
const progressStore = useProgressStore()

const loading = ref(true)
const topic = ref<Topic | null>(null)
const courses = ref<Course[]>([])
const progress = ref<UserProgress | null>(null)

const topicId = Number(route.params.id)

onMounted(async () => {
  const [coursesData, prog] = await Promise.all([
    topicStore.fetchCourses(topicId),
    progressStore.fetchForTopic(topicId),
  ])
  courses.value = coursesData
  progress.value = prog
  topic.value = topicStore.topics.find((t) => t.id === topicId) ?? null
  if (!topic.value) await topicStore.fetchTopics().then(() => {
    topic.value = topicStore.topics.find((t) => t.id === topicId) ?? null
  })
  loading.value = false
})

function isCompleted(unitId: number) {
  return progress.value?.completed_unit_ids.includes(unitId) ?? false
}

function goToLesson(unitId: number) {
  router.push({ name: 'lesson', params: { unitId } })
}
</script>
