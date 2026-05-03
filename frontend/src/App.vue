<template>
  <div class="min-h-screen bg-gray-50 flex flex-col">
    <!-- Desktop sidebar + content layout -->
    <div class="flex flex-1">
      <!-- Sidebar (desktop only) -->
      <SideBar v-if="!isLessonRoute" class="hidden lg:flex" />

      <!-- Main content -->
      <main class="flex-1 min-w-0" :class="{ 'lg:ml-64': !isLessonRoute }">
        <!-- Mobile top bar -->
        <MobileTopBar v-if="!isLessonRoute" class="lg:hidden" />
        <RouterView />
      </main>
    </div>

    <!-- Mobile bottom nav -->
    <MobileBottomNav v-if="!isLessonRoute" class="lg:hidden" />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import SideBar from './components/SideBar.vue'
import MobileTopBar from './components/MobileTopBar.vue'
import MobileBottomNav from './components/MobileBottomNav.vue'

const route = useRoute()
const isLessonRoute = computed(() => route.name === 'lesson')
</script>
