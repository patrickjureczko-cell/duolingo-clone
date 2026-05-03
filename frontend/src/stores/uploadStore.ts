import { defineStore } from 'pinia'
import { ref } from 'vue'
import client from '../api/client'
import { sessionId } from '../api/client'
import type { Upload } from '../api/types'

export const useUploadStore = defineStore('upload', () => {
  const current = ref<Upload | null>(null)
  const polling = ref(false)

  async function submitUpload(file: File, topicId: number, courseTitle: string): Promise<Upload> {
    const form = new FormData()
    form.append('file', file)
    form.append('topic_id', String(topicId))
    form.append('course_title', courseTitle)
    form.append('session_id', sessionId)
    const { data } = await client.post<Upload>('/uploads/', form, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    current.value = data
    return data
  }

  async function pollStatus(uploadId: number): Promise<Upload> {
    polling.value = true
    return new Promise((resolve, reject) => {
      const interval = setInterval(async () => {
        try {
          const { data } = await client.get<Upload>(`/uploads/${uploadId}/`)
          current.value = data
          if (data.status === 'done' || data.status === 'failed') {
            clearInterval(interval)
            polling.value = false
            resolve(data)
          }
        } catch (e) {
          clearInterval(interval)
          polling.value = false
          reject(e)
        }
      }, 2000)
    })
  }

  return { current, polling, submitUpload, pollStatus }
})
