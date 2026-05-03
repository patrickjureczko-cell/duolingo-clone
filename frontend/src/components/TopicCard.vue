<template>
  <RouterLink
    :to="`/topic/${topic.id}`"
    class="card flex items-center gap-4 hover:scale-[1.02] transition-transform cursor-pointer"
    :style="{ borderColor: topic.color }"
  >
    <div
      class="w-16 h-16 rounded-2xl flex items-center justify-center text-3xl flex-shrink-0"
      :style="{ backgroundColor: topic.color + '22' }"
    >
      {{ topic.icon }}
    </div>
    <div class="flex-1 min-w-0">
      <div class="font-extrabold text-lg text-duo-dark">{{ topic.name }}</div>
      <div class="text-sm text-duo-gray line-clamp-2">{{ topic.description }}</div>
      <div v-if="progress" class="mt-1">
        <div class="flex items-center gap-2 text-xs font-bold text-duo-gray">
          <div class="flex-1 bg-duo-light-gray rounded-full h-2">
            <div class="h-2 rounded-full transition-all" :style="{ width: xpBarWidth, backgroundColor: topic.color }" />
          </div>
          <span>{{ progress.xp }} XP</span>
        </div>
      </div>
    </div>
    <div class="text-duo-gray text-xl">›</div>
  </RouterLink>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { Topic, UserProgress } from '../api/types'

const props = defineProps<{ topic: Topic; progress?: UserProgress }>()

const xpBarWidth = computed(() => {
  const xp = props.progress?.xp ?? 0
  return Math.min(100, (xp / 500) * 100) + '%'
})
</script>
