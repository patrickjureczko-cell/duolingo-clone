import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

const apiBase = process.env.VITE_API_BASE || 'http://localhost:8000'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 5173,
    proxy: {
      '/api': apiBase,
      '/media': apiBase,
    },
  },
})
