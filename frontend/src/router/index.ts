import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'home', component: HomeView },
    { path: '/topic/:id', name: 'topic', component: () => import('../views/TopicView.vue') },
    { path: '/lesson/:unitId', name: 'lesson', component: () => import('../views/LessonView.vue') },
    { path: '/upload', name: 'upload', component: () => import('../views/UploadView.vue') },
  ],
})

export default router
