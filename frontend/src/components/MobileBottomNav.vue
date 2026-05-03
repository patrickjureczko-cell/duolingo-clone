<template>
  <nav class="fixed bottom-0 left-0 right-0 bg-white border-t-2 border-duo-light-gray flex z-20 pb-safe">
    <RouterLink v-for="item in navItems" :key="item.to" :to="item.to"
      class="flex-1 flex flex-col items-center gap-1 py-3 text-duo-gray font-bold text-xs transition-colors"
      active-class="!text-duo-green"
    >
      <span class="text-2xl">{{ item.icon }}</span>
      <span>{{ item.label }}</span>
    </RouterLink>
  </nav>
</template>

<script setup lang="ts">
const navItems = [
  { to: '/', icon: '🏠', label: 'Learn' },
  { to: '/upload', icon: '📄', label: 'Upload' },
]
</script>
