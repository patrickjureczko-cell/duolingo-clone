<template>
  <div class="min-h-screen bg-gray-50">
    <NavBar v-if="!isLessonRoute" />
    <RouterView />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import NavBar from './components/NavBar.vue'

const route = useRoute()
const isLessonRoute = computed(() => route.name === 'lesson')
</script>
