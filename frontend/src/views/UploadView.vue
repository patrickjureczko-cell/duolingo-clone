<template>
  <main class="max-w-lg mx-auto px-4 py-10">
    <RouterLink to="/" class="text-duo-blue font-bold text-sm mb-6 inline-block">← Back</RouterLink>
    <h1 class="text-3xl font-extrabold text-duo-dark mb-2">Upload Material</h1>
    <p class="text-duo-gray mb-8">Upload a PDF or text file and we'll generate a full lesson from it using AI.</p>

    <!-- Upload form -->
    <div v-if="!upload.current || upload.current.status === 'failed'" class="card">
      <form @submit.prevent="handleSubmit" class="flex flex-col gap-4">
        <div>
          <label class="block font-bold text-sm text-duo-dark mb-1">Topic</label>
          <select v-model="selectedTopicId" class="w-full border-2 border-duo-light-gray rounded-xl px-3 py-2 font-semibold focus:outline-none focus:border-duo-blue" required>
            <option value="" disabled>Select a topic…</option>
            <option v-for="t in topicStore.topics" :key="t.id" :value="t.id">
              {{ t.icon }} {{ t.name }}
            </option>
          </select>
        </div>

        <div>
          <label class="block font-bold text-sm text-duo-dark mb-1">Course name</label>
          <input
            v-model="courseTitle"
            type="text"
            placeholder="e.g. Introduction to Networking"
            class="w-full border-2 border-duo-light-gray rounded-xl px-3 py-2 font-semibold focus:outline-none focus:border-duo-blue"
            required
          />
        </div>

        <div>
          <label class="block font-bold text-sm text-duo-dark mb-1">File (PDF or .txt)</label>
          <div
            class="border-2 border-dashed border-duo-light-gray rounded-xl p-6 text-center cursor-pointer hover:border-duo-blue transition-colors"
            @click="fileInput?.click()"
            @dragover.prevent
            @drop.prevent="onDrop"
          >
            <div v-if="!selectedFile">
              <div class="text-4xl mb-2">📄</div>
              <div class="font-bold text-duo-gray">Click or drag a file here</div>
              <div class="text-xs text-duo-gray mt-1">PDF, TXT — max 20 MB</div>
            </div>
            <div v-else class="font-bold text-duo-blue">{{ selectedFile.name }}</div>
          </div>
          <input ref="fileInput" type="file" accept=".pdf,.txt" class="hidden" @change="onFileChange" />
        </div>

        <div v-if="upload.current?.status === 'failed'" class="text-duo-red text-sm font-bold">
          ⚠️ {{ upload.current.error_message || 'Processing failed. Please try again.' }}
        </div>

        <button type="submit" class="btn-primary" :disabled="!selectedFile || !selectedTopicId || submitting">
          {{ submitting ? 'Uploading…' : 'Generate Lesson' }}
        </button>
      </form>
    </div>

    <!-- Processing state -->
    <div v-else-if="upload.current.status === 'pending' || upload.current.status === 'processing'" class="card text-center py-10">
      <div class="w-12 h-12 border-4 border-duo-green border-t-transparent rounded-full animate-spin mx-auto mb-4" />
      <div class="font-extrabold text-duo-dark text-lg mb-1">Generating your lesson…</div>
      <div class="text-duo-gray text-sm">Claude is reading your file and creating questions.</div>
    </div>

    <!-- Done state -->
    <div v-else-if="upload.current.status === 'done'" class="card text-center py-10">
      <div class="text-5xl mb-4">🎉</div>
      <div class="font-extrabold text-duo-dark text-xl mb-1">Lesson ready!</div>
      <div class="text-duo-gray mb-6">
        Created <strong>{{ upload.current.questions_created }}</strong> questions for
        <strong>{{ upload.current.course_title }}</strong>.
      </div>
      <RouterLink
        v-if="upload.current.course"
        :to="`/topic/${upload.current.topic}`"
        class="btn-primary inline-block"
      >
        Start Learning
      </RouterLink>
    </div>
  </main>
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

onMounted(() => {
  upload.current = null
  topicStore.fetchTopics()
})

function onFileChange(e: Event) {
  const input = e.target as HTMLInputElement
  if (input.files?.[0]) selectedFile.value = input.files[0]
}

function onDrop(e: DragEvent) {
  if (e.dataTransfer?.files?.[0]) selectedFile.value = e.dataTransfer.files[0]
}

async function handleSubmit() {
  if (!selectedFile.value || !selectedTopicId.value) return
  submitting.value = true
  const result = await upload.submitUpload(selectedFile.value, Number(selectedTopicId.value), courseTitle.value)
  submitting.value = false
  upload.pollStatus(result.id)
}
</script>
