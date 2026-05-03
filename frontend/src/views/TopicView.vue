<template>
  <div class="max-w-lg mx-auto px-4 py-6 pb-28 lg:pb-8">
    <!-- Back -->
    <RouterLink to="/" class="inline-flex items-center gap-1 text-duo-gray font-bold text-sm mb-4 hover:text-duo-dark">
      ← Back
    </RouterLink>

    <!-- Loading skeleton -->
    <div v-if="loading" class="space-y-4">
      <div class="h-24 card animate-pulse" />
      <div class="h-16 card animate-pulse" />
    </div>

    <template v-else>
      <!-- Topic header -->
      <div class="card p-5 flex items-center gap-4 mb-4">
        <div class="w-16 h-16 rounded-2xl flex items-center justify-center text-4xl"
          :style="{ background: (topic?.color ?? '#58CC02') + '22' }">
          {{ topic?.icon }}
        </div>
        <div class="flex-1">
          <h1 class="text-xl font-extrabold text-duo-dark">{{ topic?.name }}</h1>
          <p class="text-sm text-duo-gray">{{ topic?.description }}</p>
        </div>
      </div>

      <!-- Stats row -->
      <div class="grid grid-cols-3 gap-3 mb-6">
        <div class="card p-3 text-center">
          <div class="text-2xl font-extrabold text-duo-orange">🔥{{ progress?.streak_days ?? 0 }}</div>
          <div class="text-xs text-duo-gray font-bold mt-0.5">Streak</div>
        </div>
        <div class="card p-3 text-center">
          <div class="text-2xl font-extrabold text-yellow-500">⭐{{ progress?.xp ?? 0 }}</div>
          <div class="text-xs text-duo-gray font-bold mt-0.5">XP</div>
        </div>
        <div class="card p-3 text-center">
          <div class="text-xl font-extrabold text-duo-red leading-tight mt-0.5">
            {{ '❤️'.repeat(progress?.hearts ?? 5) }}
          </div>
          <div class="text-xs text-duo-gray font-bold mt-0.5">Hearts</div>
        </div>
      </div>

      <!-- Empty state with generate -->
      <div v-if="courses.length === 0" class="card p-8 text-center">
        <div class="text-6xl mb-4">🤖</div>
        <h2 class="font-extrabold text-xl text-duo-dark mb-1">No lessons yet</h2>
        <p class="text-duo-gray text-sm mb-6">
          Let AI generate a course for you, or upload your own material.
        </p>
        <div class="flex flex-col gap-3">
          <button class="btn-primary w-full" :disabled="generating" @click="autoGenerate">
            {{ generating ? '✨ Generating…' : '✨ Generate with AI' }}
          </button>
          <RouterLink to="/upload" class="btn-secondary w-full text-center">📄 Upload Material</RouterLink>
        </div>
        <div v-if="generating" class="mt-4 text-sm text-duo-gray animate-pulse">
          AI is creating your first lesson…
        </div>
      </div>

      <!-- Course path -->
      <div v-for="course in courses" :key="course.id" class="mb-8">
        <!-- Course header -->
        <div class="flex items-center justify-between mb-4 px-1">
          <div>
            <h2 class="font-extrabold text-duo-dark text-lg leading-tight">{{ course.title }}</h2>
            <p v-if="course.description" class="text-xs text-duo-gray">{{ course.description }}</p>
          </div>
          <span class="text-xs bg-duo-light-gray text-duo-gray px-3 py-1 rounded-full font-bold">
            {{ course.units.length }} unit{{ course.units.length !== 1 ? 's' : '' }}
          </span>
        </div>

        <!-- Path map -->
        <div class="relative">
          <!-- Vertical path line -->
          <div class="absolute left-1/2 top-10 bottom-10 w-1 bg-duo-light-gray -translate-x-1/2 rounded-full" />

          <div
            v-for="(unit, idx) in course.units"
            :key="unit.id"
            class="relative mb-10 flex"
            :class="pathAlignment(idx)"
          >
            <!-- Connector dot on center line -->
            <div
              v-if="idx > 0"
              class="absolute top-[-2.5rem] left-1/2 -translate-x-1/2 w-3 h-3 rounded-full border-2"
              :class="isCompleted(unit.id) ? 'bg-duo-green border-duo-green' : 'bg-white border-duo-light-gray'"
            />

            <!-- Node -->
            <div class="flex flex-col items-center gap-2" style="width: 90px">
              <button
                class="unit-node"
                :class="nodeClass(unit)"
                :disabled="unit.question_count === 0"
                @click="unit.question_count > 0 && goToLesson(unit.id)"
              >
                <span v-if="isCompleted(unit.id)">✓</span>
                <span v-else>{{ idx + 1 }}</span>
              </button>
              <span class="text-xs font-bold text-duo-gray text-center leading-tight px-1">
                {{ unit.title }}
              </span>
              <span v-if="unit.question_count === 0" class="text-xs text-duo-gray/60">No questions</span>
              <span v-else class="text-xs font-bold"
                :class="isCompleted(unit.id) ? 'text-duo-green' : 'text-duo-blue'">
                {{ unit.question_count }} Q
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- Generate more (when courses exist) -->
      <div v-if="courses.length > 0" class="card p-4 flex items-center gap-3 mt-2">
        <div class="text-2xl">✨</div>
        <div class="flex-1">
          <div class="font-bold text-duo-dark text-sm">Want more content?</div>
          <div class="text-xs text-duo-gray">Generate another AI course</div>
        </div>
        <button class="btn-primary !py-2 !px-4 !text-xs" :disabled="generating" @click="autoGenerate">
          {{ generating ? '…' : 'Generate' }}
        </button>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import client from '../api/client'
import { sessionId } from '../api/client'
import { useTopicStore } from '../stores/topicStore'
import { useProgressStore } from '../stores/progressStore'
import type { Topic, Course, Unit, UserProgress } from '../api/types'

const route = useRoute()
const router = useRouter()
const topicStore = useTopicStore()
const progressStore = useProgressStore()

const loading = ref(true)
const generating = ref(false)
const topic = ref<Topic | null>(null)
const courses = ref<Course[]>([])
const progress = ref<UserProgress | null>(null)
const topicId = Number(route.params.id)

onMounted(async () => {
  await topicStore.fetchTopics()
  topic.value = topicStore.topics.find((t) => t.id === topicId) ?? null
  const [c, p] = await Promise.all([
    topicStore.fetchCourses(topicId),
    progressStore.fetchForTopic(topicId),
  ])
  courses.value = c
  progress.value = p
  loading.value = false
})

function isCompleted(unitId: number) {
  return progress.value?.completed_unit_ids.includes(unitId) ?? false
}

function pathAlignment(idx: number) {
  const col = idx % 3
  if (col === 0) return 'justify-start pl-4'
  if (col === 1) return 'justify-center'
  return 'justify-end pr-4'
}

function nodeClass(unit: Unit) {
  if (unit.question_count === 0)
    return 'bg-duo-gray border-gray-400 opacity-40 cursor-not-allowed'
  if (isCompleted(unit.id))
    return 'bg-duo-green border-duo-green-dark cursor-pointer'
  return 'bg-duo-blue border-blue-700 cursor-pointer hover:brightness-110'
}

function goToLesson(unitId: number) {
  router.push({ name: 'lesson', params: { unitId } })
}

async function autoGenerate() {
  if (!topic.value || generating.value) return
  generating.value = true
  try {
    const { data } = await client.post(`/topics/${topicId}/generate/`, {
      session_id: sessionId,
    })
    // Poll upload status until done
    const poll = setInterval(async () => {
      const { data: status } = await client.get(`/uploads/${data.upload_id}/`)
      if (status.status === 'done') {
        clearInterval(poll)
        generating.value = false
        const newCourses = await topicStore.fetchCourses(topicId)
        courses.value = newCourses
      } else if (status.status === 'failed') {
        clearInterval(poll)
        generating.value = false
      }
    }, 2000)
  } catch {
    generating.value = false
  }
}
</script>
