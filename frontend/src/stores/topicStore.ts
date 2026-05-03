import { defineStore } from 'pinia'
import { ref } from 'vue'
import client from '../api/client'
import type { Topic, Course } from '../api/types'

export const useTopicStore = defineStore('topics', () => {
  const topics = ref<Topic[]>([])
  const loading = ref(false)

  async function fetchTopics() {
    loading.value = true
    const { data } = await client.get<{ results: Topic[] }>('/topics/')
    topics.value = data.results ?? data
    loading.value = false
  }

  async function fetchCourses(topicId: number): Promise<Course[]> {
    const { data } = await client.get<{ results: Course[] }>(`/courses/?topic=${topicId}`)
    return data.results ?? data
  }

  return { topics, loading, fetchTopics, fetchCourses }
})
