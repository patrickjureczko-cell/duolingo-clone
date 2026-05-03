import { defineStore } from 'pinia'
import { ref } from 'vue'
import client from '../api/client'
import { sessionId } from '../api/client'
import type { UserProgress } from '../api/types'

export const useProgressStore = defineStore('progress', () => {
  const allProgress = ref<UserProgress[]>([])

  async function fetchAll() {
    const { data } = await client.get<UserProgress[]>(`/progress/${sessionId}/`)
    allProgress.value = data
  }

  async function fetchForTopic(topicId: number): Promise<UserProgress> {
    const { data } = await client.get<UserProgress>(`/progress/${sessionId}/topic/${topicId}/`)
    const idx = allProgress.value.findIndex((p) => p.topic === topicId)
    if (idx >= 0) allProgress.value[idx] = data
    else allProgress.value.push(data)
    return data
  }

  function getForTopic(topicId: number): UserProgress | undefined {
    return allProgress.value.find((p) => p.topic === topicId)
  }

  return { allProgress, fetchAll, fetchForTopic, getForTopic }
})
