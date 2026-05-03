<template>
  <div class="max-w-lg mx-auto px-4 py-8 pb-28 lg:pb-8">
    <RouterLink to="/" class="inline-flex items-center gap-1 text-duo-gray font-bold text-sm mb-6 hover:text-duo-dark">
      ← Back
    </RouterLink>
    <h1 class="text-2xl font-extrabold text-duo-dark mb-1">Upload Material</h1>
    <p class="text-duo-gray text-sm mb-6">Upload a PDF or text file and AI will generate a full lesson from it.</p>

    <!-- Form -->
    <div v-if="!upload.current || upload.current.status === 'failed'" class="card p-6 flex flex-col gap-5">
      <div>
        <label class="block font-extrabold text-sm text-duo-dark mb-1.5">Topic</label>
        <select v-model="selectedTopicId" required
          class="w-full border-2 border-duo-light-gray rounded-2xl px-4 py-3 font-bold focus:outline-none focus:border-duo-blue bg-white">
          <option value="" disabled>Select a topic…</option>
          <option v-for="t in topicStore.topics" :key="t.id" :value="t.id">{{ t.icon }} {{ t.name }}</option>
        </select>
      </div>

      <div>
        <label class="block font-extrabold text-sm text-duo-dark mb-1.5">Course name</label>
        <input v-model="courseTitle" type="text" placeholder="e.g. Introduction to Networking"
          class="w-full border-2 border-duo-light-gray rounded-2xl px-4 py-3 font-bold focus:outline-none focus:border-duo-blue" />
      </div>

      <!-- Drop zone -->
      <div>
        <label class="block font-extrabold text-sm text-duo-dark mb-1.5">File</label>
        <div
          class="border-2 border-dashed rounded-2xl p-8 text-center cursor-pointer transition-colors"
          :class="selectedFile ? 'border-duo-green bg-green-50' : 'border-duo-light-gray hover:border-duo-blue hover:bg-blue-50'"
          @click="fileInput?.click()"
          @dragover.prevent
          @drop.prevent="onDrop"
        >
          <div v-if="!selectedFile" class="flex flex-col items-center gap-2">
            <div class="text-4xl">📄</div>
            <div class="font-bold text-duo-gray">Click or drag a file here</div>
            <div class="text-xs text-duo-gray/70">PDF or TXT — max 20 MB</div>
          </div>
          <div v-else class="flex items-center justify-center gap-2 font-bold text-duo-green">
            <span class="text-2xl">✅</span> {{ selectedFile.name }}
          </div>
        </div>
        <input ref="fileInput" type="file" accept=".pdf,.txt" class="hidden" @change="onFileChange" />
      </div>

      <div v-if="upload.current?.status === 'failed'"
        class="bg-red-50 border border-duo-red rounded-2xl p-3 text-duo-red text-sm font-semibold">
        ⚠️ {{ upload.current.error_message || 'Processing failed. Try again.' }}
      </div>

      <button class="btn-primary w-full" :disabled="!selectedFile || !selectedTopicId || submitting" @click="handleSubmit">
        {{ submitting ? 'Uploading…' : '✨ Generate Lesson' }}
      </button>
    </div>

    <!-- Processing -->
    <div v-else-if="['pending','processing'].includes(upload.current.status)"
      class="card p-10 text-center">
      <div class="w-16 h-16 border-4 border-duo-green border-t-transparent rounded-full animate-spin mx-auto mb-5" />
      <div class="font-extrabold text-duo-dark text-xl mb-1">Generating your lesson…</div>
      <div class="text-duo-gray text-sm">AI is reading your file and crafting questions.</div>
      <div class="mt-4 flex justify-center gap-1">
        <span v-for="i in 3" :key="i" class="w-2 h-2 rounded-full bg-duo-green animate-bounce"
          :style="{ animationDelay: `${i * 0.15}s` }" />
      </div>
    </div>

    <!-- Done -->
    <div v-else-if="upload.current.status === 'done'" class="card p-10 text-center">
      <div class="text-6xl mb-4">🎉</div>
      <div class="font-extrabold text-duo-dark text-2xl mb-1">Lesson Ready!</div>
      <div class="text-duo-gray mb-2">
        <strong>{{ upload.current.questions_created }}</strong> questions created for
        <strong>{{ upload.current.course_title }}</strong>
      </div>
      <div class="flex flex-col gap-3 mt-6">
        <RouterLink :to="`/topic/${upload.current.topic}`" class="btn-primary w-full text-center">
          Start Learning →
        </RouterLink>
        <button class="btn-secondary w-full" @click="upload.current = null">Upload Another</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useUploadStore } from '../stores/uploadStore'
import { useTopicStore } from '../stores/topicStore'

const upload = useUploadStore()
const topicStore = useTopicStore()

const selectedTopicId = ref<number | ''>('')
const courseTitle = ref('')
const selectedFile = ref<File | null>(null)
const fileInput = ref<HTMLInputElement | null>(null)
const submitting = ref(false)

onMounted(() => { upload.current = null; topicStore.fetchTopics() })

function onFileChange(e: Event) {
  const f = (e.target as HTMLInputElement).files?.[0]
  if (f) selectedFile.value = f
}
function onDrop(e: DragEvent) {
  const f = e.dataTransfer?.files?.[0]
  if (f) selectedFile.value = f
}
async function handleSubmit() {
  if (!selectedFile.value || !selectedTopicId.value) return
  submitting.value = true
  const result = await upload.submitUpload(selectedFile.value, Number(selectedTopicId.value), courseTitle.value || selectedFile.value.name)
  submitting.value = false
  upload.pollStatus(result.id)
}
</script>
